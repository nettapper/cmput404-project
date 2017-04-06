import * as types from '../types';
import uuidv4 from 'uuid/v4';

import {URL_PREFIX} from '../constants';
import {getUUIDFromId} from '../utils';
/*eslint-enable */
/*
* Adds a comment, to a post specified by postId
*/
// TODO: Add post origin to comment body
export function addComment(comment, postId, postOrigin, user) {
  return function(dispatch) {
    const requestBody = {
      query: 'addComment',
      post: postOrigin,
      comment: {
        comment,
        author: {
          id: user.id,
          displayName: user.displayName,
          host: user.host,
          url: user.url
        },
        published: new Date().toISOString(),
        id: uuidv4(),
        contentType: 'text/plain'
      }
    };

    let postUUID = postId;
    if (/^http/.test(postId)) {
      postUUID = /\/([a-zA-Z0-9-]+)\/?$/.exec(postId, 'g')[1];
    }

    fetch(`${URL_PREFIX}/posts/${String(postUUID)}/comments/`, {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${btoa(`${user.username}:${user.password}`)}`, 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(requestBody),
    })
    .then(res => res.json())
    .then((res) => {
      dispatch({
        type:types.ADD_COMMENT,
        commentData: requestBody.comment,
        postId: postId
      });
     // location.reload();
    })
    .catch((err) => {

    });
  };
}
/*
* Adds a post by a user then returns an action to update the state
*/
export function addPost(post, user) {

  return function(dispatch) {

    const sendPost = function(post, user) {
      fetch(`${URL_PREFIX}/posts/`, {
        method: 'POST',
        headers: {
          // Written by unyo (http://stackoverflow.com/users/2077884/unyo http://stackoverflow.com/a/35780539 (MIT)
          'Authorization': `Basic ${btoa(`${user.username}:${user.password}`)}`, 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          title: post.title,
          content: post.content,
          description: post.description,
          contentType: post.contentType,
          author: user.id,
          comments: post.comments,
          visibility:post.permission,
          image: post.image,
          visibleTo: post.user_with_permission,
          unlisted:post.unlisted,
        }),
      })
      .then(res => res.json())
      .then((res) => {
        dispatch({type:types.ADD_POST,post: res});
      })
      .catch((err) => { });
    };

    if (post.image){
      const FR= new FileReader();
      FR.addEventListener("load", function(e) {
        post.content = e.target.result;
        post.contentType = `${post.image.type};base64`;
        sendPost(post,user);
      }); 
      FR.readAsDataURL( post.image );
    }else{
      sendPost(post,user);
    }
  };
}

/*
* Returns an action with the post results (or [])
*/
function finishLoadingPosts(result) {
  return {
    type: types.FINISH_LOADING_POSTS,
    posts: result || [],
    authors: []
  };
}

/*
* Loads all posts visible to the current user
*/
export function loadPosts(user) {
  return function(dispatch) {
    return fetch(`${URL_PREFIX}/author/posts/`,{
      method: 'GET',
      headers: {
        // Written by unyo (http://stackoverflow.com/users/2077884/unyo http://stackoverflow.com/a/35780539 (MIT)
        'Authorization': `Basic ${btoa(`${user.username}:${user.password}`)}`,
        'Accept': 'application/json'
      }
    })
      .then(res => res.json())
      .then(res => {
        dispatch(finishLoadingPosts(res));
      });
  };
}

/*
* Action that updates the state to log the user in
*/
function logIn(user) {
  return {
    type: types.LOGGED_IN,
    user
  };
}

/*
* Action that updates the state to say the log in has failed
*/
function logInFail(user) {
  return {
    type: types.LOGGED_IN_FAILED,
    user
  };
}

/*
* Attempts to log into the web service using the username and password, will return an action that specifies it failed or suceeded
*/
export function attempLogin(username, password) {
  return function(dispatch) {
    return fetch(`${URL_PREFIX}/login/`, {
      method: 'POST',
      headers: {
        // Written by unyo (http://stackoverflow.com/users/2077884/unyo http://stackoverflow.com/a/35780539 (MIT)
        'Authorization': `Basic ${btoa(`${username}:${password}`)}`
      }
    }).then(res => {
      if (!res.ok) {
        return Promise.reject(res);
      }
      return res;
    })
    .then(res => res.json())
    .then(res => {
      dispatch(logIn({
        ...res,
        username,
        password
      }));
    })
    .catch(err => {
      console.log(err);
      return dispatch(logInFail({
        ...err,
        password
      }));
    });
  };
}

/*
* Attempts to register the user to the service using the username and password
* can fail if the username is not unique
*/
export function attemptRegister(username, password, displayName) {
  return function(dispatch) {
    return fetch(`${URL_PREFIX}/register/`, {
      method: 'POST',
      headers: {
        // Written by unyo (http://stackoverflow.com/users/2077884/unyo http://stackoverflow.com/a/35780539 (MIT)
        'Authorization': `Basic ${btoa(`${username}:${password}`)}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username,
        password,
        displayName
      }),
    }).then(res => {
      if (!res.ok) {
        return Promise.reject();
      }
      return res;
    })
    .catch(err => {
      console.log('Could not register user');
    });
    // TODO: Do something when successfully registered
  };
}


/*
* Action that updates the state to say the log in has failed
*/
function updateUser(user) {
  return {
    type: types.UPDATE_USER,
    user
  };
}

export function attemptUpdateProfile(user) {
  return function(dispatch) {
    return fetch(user.url, {
      method: 'PUT',
      headers: {
        // Written by unyo (http://stackoverflow.com/users/2077884/unyo http://stackoverflow.com/a/35780539 (MIT)
        'Authorization': `Basic ${btoa(`${user.username}:${user.password}`)}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(user),
    }).then(res => {
      if (!res.ok) {
        return Promise.reject(res);
      }
      return res;
    })
    .then(res => res.json())
    .then(res => {
      dispatch(updateUser({
        ...res,
      }));
    })
    .catch(err => {
      //TODO Something on fail
    });
  };
}

/*
* Returns an action to update the user with all current users
*/
export function finishedGettingUsers(users) {
  return {
    type: types.LOADED_USERS,
    users
  };
}

/*
* Gets all of the current users, friends, and following and joins them into one with an isFriend and isFollowing
*/
export function getUsers(user) {
  return function(dispatch) {
    fetch(`${URL_PREFIX}/authors/`, {
      method: 'GET',
      headers: {
        // Written by unyo (http://stackoverflow.com/users/2077884/unyo http://stackoverflow.com/a/35780539 (MIT)
        'Authorization': `Basic ${btoa(`${user.username  }:${  user.password}`)}`
      }
    })
    .then(res => {
      if (!res.ok) {
        return Promise.reject();
      }
      return res;
    })
    .then(res => res.json())
    .then(res => {
      return dispatch(finishedGettingUsers(res));
    })
    .catch(err => {
      console.log(err, 'Could not get friends');
    });
  };
}

function followUser(currentUser, otherUser) {
  return fetch(`${URL_PREFIX}/friendrequest/`, {
    method: 'POST',
    headers: {
      // Written by unyo (http://stackoverflow.com/users/2077884/unyo http://stackoverflow.com/a/35780539 (MIT)
      'Authorization': `Basic ${btoa(`${currentUser.username}:${currentUser.password}`)}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query: 'friendrequest',
      author: {
        id: currentUser.id,
        host: currentUser.host,
        url: currentUser.url,
        displayName: currentUser.displayName
      },
      friend: {
        id: otherUser.id,
        host: otherUser.host,
        url: otherUser.url,
        displayName: otherUser.displayName
      }
    }),
  });
}

function unfollowUser(currentUser, otherUser) {
  return fetch(`${URL_PREFIX}/author/${getUUIDFromId(currentUser.id)}/friends/${getUUIDFromId(otherUser.id)}/`, {
    method: 'DELETE',
    headers: {
      // Written by unyo (http://stackoverflow.com/users/2077884/unyo http://stackoverflow.com/a/35780539 (MIT)
      'Authorization': `Basic ${btoa(`${currentUser.username}:${currentUser.password}`)}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query: 'friendrequest',
      author: {
        id: currentUser.id,
        host: currentUser.host,
        url: currentUser.url,
        displayName: currentUser.displayName
      },
      friend: {
        id: otherUser.id,
        host: otherUser.host,
        url: otherUser.url,
        displayName: otherUser.displayName
      }
    })
  });
}

export function toggleFollowStatus(currentUser, otherUser, isFriend) {
  return function(dispatch) {
    const toggleFollow = isFriend ? unfollowUser : followUser;

    return toggleFollow(currentUser, otherUser)
    .then(res => {
      if (!res.ok) {
        return Promise.reject();
      }
      return res;
    })
    .catch(err => {
      console.log('Could not toggle follow status');
    });
  };
}

/*
* Deletes a post specified by post
*/
export function deletePost(post, user){
  return function(dispatch) {
    fetch(`${URL_PREFIX}/posts/${post.id}/`, {
      method: 'DELETE',
      headers: {
        // Written by unyo (http://stackoverflow.com/users/2077884/unyo http://stackoverflow.com/a/35780539 (MIT)
        'Authorization': `Basic ${btoa(`${user.username}:${user.password}`)}`
      },
    })
    .then(res => {
      if (!res.ok) {
        return Promise.reject();
      }
      return res;
    })
    .then((res) => {
      dispatch({type:types.DELETE_POST,post:post});
    })
    .catch((err) => {
      console.log('Could not delete post', err);
    });
  };
}


/*
* Get a post specified by post
*/
export function getPost(id, user){
  return function(dispatch) {
    fetch(`${URL_PREFIX}/posts/${id}/`, {
      method: 'GET',
      headers: {
        // Written by unyo (http://stackoverflow.com/users/2077884/unyo http://stackoverflow.com/a/35780539 (MIT)
        'Authorization': `Basic ${btoa(`${user.username}:${user.password}`)}`
      },
    })
    .then(res => res.json())
      .then(res => {
        // console.log(res)
        dispatch(finishLoadingPosts([res]));
      });
  };
}


