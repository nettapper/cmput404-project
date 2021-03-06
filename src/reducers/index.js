/*
MIT License

Copyright (c) 2017 Conner Dunn, Tian Zhi Wang, Kyle Carlstrom, Xin Yi Wang, Josh Deng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
import { combineReducers } from 'redux';
import * as types from '../types';

/**
 * Posts Reducer
 * @param [] state 
 * @param {} action 
 */
export function posts(state=[], action) {
  switch (action.type) {
    /**
     * Add Comment to state [ post : { comments: List } ]
     * @param [] state 
     * @param { type: Enum, postId: Number, comment: Object} action
     */
  case types.ADD_COMMENT:
    return state.map(post => {
      if (post.id === action.postId) {
        return {
          ...post,
          comments: [
            ...post.comments,
            action.commentData
          ]
        };
      }
      return post;
    });
    /**
     * Add Post to state []
     * @param [] state 
     * @param { type: Enum, post: Object } action
     */
  case types.ADD_POST:
    return [
      action.post,
      ...state
    ];
      /**
     * Update Post in state []
     * @param [] state 
     * @param { type: Enum, post: Object } action
     */
  case types.UPDATE_POST:
    const filterself = state.filter(function rm(value){
      return value.id != action.post.id;
    });
    return [
      action.post,
      ...filterself
    ];
    /**
     * Finish Loading Post
     * @param [] state 
     * @param { type: Enum, post: Object } action
     */
  case types.FINISH_LOADING_POSTS:
    return action.posts;
    /**
     * Delete Post from state []
     * @param [] state 
     * @param { type: Enum, post: Object } action
     */
  case types.DELETE_POST:
    const temp = state.filter(function rm(value){
      return value.id!= action.post.id;
    }
      );
    return temp;

  default:
    return state;
  }
}

/**
 * App Reducer
 * @param [] state 
 * @param {} action 
 */
export function app(state={loggedIn: false, activeTab: 'stream'}, action) {
  switch (action.type) {
    /**
     * Log In, add  { loggedIn: true } to state [ app : {} ]
     * @param [] state 
     * @param { type: Enum, user: Object } action
     */
  case types.LOGGED_IN:
    return {
      ...state,
      loggedIn: true,
      user: action.user
    };
    /**
   * Log Out, add  { loggedIn: true } to state [ app : {} ]
   * @param [] state 
   * @param { type: Enum} action
   */
  case types.LOGGED_OUT:
    return {
      ...state,
      loggedIn: false
    };
    /**
     * Log In Failure, add { loggedInFail: true} { loggedIn: false } to state [ app : {} ]
     * @param [] state 
     * @param { type: Enum, user: Object } action
     */
  case types.LOGGED_IN_FAILED:
    return {
      ...state,
      loggedIn: false,
      loggedInFail: true,
      user: action.user
    };
    /**
     * Update User
     * @param [] state 
     * @param { type: Enum, user: Object } action
     */
  case types.UPDATE_USER:
    return {
      ...state,
      user: {...state.user,
        ...action.user},
      viewUser: {...state.user,
        ...action.user}
    };
  /**
     * Switch Tabs, sets the active tab in state [ app : {} ]
     * @param [] state 
     * @param { type: Enum, tab: Object } action
     */
  case types.SWITCH_TABS:
    return {
      ...state,
      activeTab: action.tab,
      viewUser: action.user ? action.user : state.user
    };
  default:
    return state;
  }
}


export function github(state=[], action) {
  switch (action.type) {

  case types.LOAD_GITHUB:
    return action.githubEvents;

  default:
    return state;
  }
}

/**
 * Combine reducers to a a single reducer
 */
export default combineReducers({posts, app, github});
