# -*- coding: utf-8 -*-
# Implementation from https://dev.to/davidisrawi/build-a-quick-summarizer-with-python-and-nltk

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk

nltk.download("punkt")
nltk.download("stopwords")


# All weightage for structure doc
# Important: These scores are for the experimenting purpose only
WEIGHT_FOR_LIST = 5
WEIGHT_FOR_HIGHLIGHTED = 10
WEIGHT_FOR_NUMERICAL = 5
WEIGHT_FIRST_PARAGRAPH = 5
WEIGHT_BASIC = 1


def _create_frequency_table(paragraph_list) -> dict:
    """
    we create a dictionary for the word frequency table.
    For this, we should only use the words that are not part of the stopWords array.

    Removing stop words and making frequency table
    Stemmer - an algorithm to bring words to its root word.
    :rtype: dict
    """
    stopWords = set(stopwords.words("english"))

    ps = PorterStemmer()

    freqTable = dict()
    for paragraph in paragraph_list:
        words = word_tokenize(paragraph.text)

        all_highlighted_sentences = [sent for sent in paragraph.get_highlighted()]
        highlighted_words_text = " ".join(all_highlighted_sentences)
        highlighted_words = word_tokenize(highlighted_words_text)

        for word in words:
            if paragraph.is_list_set:
                weight = WEIGHT_FOR_LIST
            else:
                weight = WEIGHT_BASIC

            if word in highlighted_words:
                weight += WEIGHT_FOR_HIGHLIGHTED

            if word.isnumeric() and len(word) >= 2:
                weight += WEIGHT_FOR_NUMERICAL

            if paragraph.is_first_paragraph:
                weight += WEIGHT_FIRST_PARAGRAPH

            word = ps.stem(word)
            if word in stopWords:
                continue

            if word in freqTable:
                freqTable[word] += weight
            else:
                freqTable[word] = weight

    return freqTable


def _score_sentences(sentences, freqTable) -> dict:
    """
    score a sentence by its words
    Basic algorithm: adding the frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """
    # TODO: Can you make this multiprocess compatible in python?

    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = len(word_tokenize(sentence))
        word_count_in_sentence_except_stop_words = 0
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                word_count_in_sentence_except_stop_words += 1
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        if sentence[:10] in sentenceValue:
            sentenceValue[sentence[:10]] = (
                sentenceValue[sentence[:10]] / word_count_in_sentence_except_stop_words
            )

        """
        Notice that a potential issue with our score algorithm is that long sentences will have an advantage over short sentences. 
        To solve this, we're dividing every sentence score by the number of words in the sentence.
        
        Note that here sentence[:10] is the first 10 character of any sentence, this is to save memory while saving keys of
        the dictionary.
        """

    return sentenceValue


def _find_average_score(sentenceValue) -> int:
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    average = 0
    # Average value of a sentence from original summary_text
    if len(sentenceValue) > 0:
        average = sumValues / len(sentenceValue)

    return average


def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ""

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (
            threshold
        ):
            summary += " " + sentence
            sentence_count += 1

    # TODO: check if the sentences in the summarization is in the original order of occurrence.

    return summary


def run_summarization(paragraph_list):
    # 1 Create the word frequency table
    freq_table = _create_frequency_table(paragraph_list)
    # print (freq_table)

    """
    We already have a sentence tokenizer, so we just need 
    to run the sent_tokenize() method to create the array of sentences.
    """

    # 2 Tokenize the sentences
    sentences = [paragraph.text for paragraph in paragraph_list]
    # print(sentences)

    # 3 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(sentences, freq_table)

    # 4 Find the threshold
    threshold = _find_average_score(sentence_scores)

    # 5 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, 1.3 * threshold)

    return summary
