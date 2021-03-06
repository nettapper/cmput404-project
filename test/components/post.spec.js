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
import React from 'react';
import { mount, shallow } from 'enzyme';
import { assert } from 'chai';
import { describe, it } from 'mocha';

import Post from '../../src/components/Post';

describe('<Post>', function () {
  const store={};
  const props = {
    addComment: function () {},
    author: { displayname: "Aaa" },
    comments: [],
    content: "",
    contentType: "",
    deletePost: function() {},
    id: 1,
    title: "Aaa",
    user: {}
  };
  it('Should render', () => {
    const wrapper = shallow(<Post {...props}/>);
    assert.equal(wrapper.find('.post').length, 1);
  });
});