const natural = require('natural');
const mimir = require('mimir');
const sw = require('stopword');
const fs = require('fs');
const csv = require('csvtojson');
const bow = mimir.bow;
const dict = mimir.dict;
var ProgressBar = require('progress');


var texts = [];
csv()
  .fromFile('./data-pre-processing.csv')
  .on('json', (jsonObj) => {
    texts.push(jsonObj.CONTENT);
  })
  .on('done', (error) => {
    preProcess(texts);
  });

function preProcess(texts) {
  var stream = fs.createWriteStream('./data-pos-processing.csv', {flags: 'w'});

  //stemming and removing stopwords
  console.log('- Stemming and stopwords');
  texts = texts.map(text => {
    //Remove Special characters
    text = text.replace(/[^\w\s]/gi, "").toLowerCase();
    //Remove stop words
    text = sw.removeStopwords(text.split(' '));
    //Stemming remaining words
    text = text.map(token => natural.PorterStemmer.stem(token)).join(' ');
    return text;
  });

  console.log('- Creating dictionary')
  let voc = dict(texts);
  voc.words.forEach(word => {
    stream.write(word + ",");
  });
  stream.write('\n');
  console.log('- Creating bag and writing to CSV file');

  texts.forEach(text => {

    bow(text, voc).forEach( result => {
      stream.write(result + ",");
    });
    stream.write('\n');
  });

}