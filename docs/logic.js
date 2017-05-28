// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/
theinput = []
function getevent(e)
{
  var words = e.target.value.split(/(\s+|-)/)
  words = words.map(function(word) {
    if (/\s+/.test(word)) {
      return word
    } else if (word === '-') {
      return '־'
    } else {
      try {
        return make_pointy(word)
      } catch (e) {
        return word
      }
    }
  })
  poo.value = words.join('')
}


Trie = function(root)
{
  this.root = root
}
Trie.prototype.getpart = function(str)
{
  var node = this.root
  var value = null
  var remainder = str
  var i
  var chr
  for (i=0; i < str.length; ++i) {
    chr = str[i]
    node = node[1][chr]
    if (node === undefined) {
      if (value === null)
        throw 'KeyError: ' + str
      else
        return {value: value, remainder: remainder}
    }
    if (node[0] !== null) {
      value = node[0]
      remainder = str.slice(i+1)
    }
  }
  if (value === null)
    throw 'KeyError' + str
  else
    return {value: value, remainder: remainder}
}
Trie.prototype.getallparts = function(str)
{
  var results = []
  var vr = {remainder: str}
  while (vr.remainder) {
    vr = this.getpart(vr.remainder)
    results.push(vr.value)
  }
  return results
}

for (t in data)
  data[t] = new Trie(data[t])

function get_end(word)
{
  word = word.split('').reverse().join('')
  var end = data.end.getpart(word)
  end.remainder = end.remainder.split('').reverse().join('')
  return end
}

punct = function()
{
  var punct = {':': '׃'}
  var punctstring = '.?,!"'
  var c
  for (var i=0; i < punctstring.length; i++) {
    c = punctstring.charAt(i)
    punct[c] = c
  }
  return punct
}()


function make_pointy(word)
{
  var end
  var front
  var middle
  var front_junk = ''
  var back_junk = ''
  
  end = get_end(word)
  if (end.remainder !== '') {
    try {
      front = data.front.getpart(end.remainder)
    } catch (e) {
      return no_end(word)
    }
  } else {
    return no_end(word)
  }
  if (front.remainder !== '') {
    middle = data.mid.getallparts(front.remainder).join('')
    return front.value + middle + end.value
  } else {
    return front.value + end.value
  }
}

function no_end(word)
{
  var front
  var end
  var middle
  front = data.front.getpart(word)
  if (front.remainder !== '') {
    end = get_end(front.remainder)
    if (end.remainder !== '') {
      middle = data.mid.getallparts(end.remainder).join('')
      return front.value + middle + end.value
    } else {
      return front.value + end.value
    }
  } else {
    return front.value
  }
}
