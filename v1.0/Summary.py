#importing libraries
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import bs4 as BeautifulSoup
import urllib.request




#fetching the content from the URL
# fetched_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/20th_century')
# fetched_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Clothing')
fetched_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Salman_Khan')
# fetched_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/GitHub')
# fetched_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Steve_Jobs')




article_read = fetched_data.read()

#parsing the URL content and storing in a variable
article_parsed = BeautifulSoup.BeautifulSoup(article_read,'html.parser')

#returning <p> tags
paragraphs = article_parsed.find_all('p')

article_content = ''

#looping through the paragraphs and adding them to the variable
for p in paragraphs:  
    article_content += p.text




def Create_Dictionary_Table(text_string) -> dict:
   
    #removing stop words
    stop_words = set(stopwords.words("english"))
    
    words = word_tokenize(text_string)
    
    #reducing words to their root form
    stem = PorterStemmer()
    
    #creating dictionary for the word frequency table
    frequency_table = dict()
    for wd in words:
        wd = stem.stem(wd)
        if wd in stop_words:
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1

    return frequency_table


def Calculate_Sentence_Scores(sentences, frequency_table) -> dict:   

    #algorithm for scoring a sentence by its words
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount = (len(word_tokenize(sentence)))
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] = frequency_table[word_weight]

        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] / sentence_wordcount_without_stop_words

       

    return sentence_weight

def Calculate_Average_Score(sentence_weight) -> int:
   
    #calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    #getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))

    return average_score



def Get_Article_Summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_Summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_Summary += " " + sentence
            sentence_counter += 1

    return article_Summary



def _run_article_summary(article):
    
    #creating a dictionary for the word frequency table
    frequency_table = Create_Dictionary_Table(article)

    #tokenizing the sentences
    sentences = sent_tokenize(article)

    #algorithm for scoring a sentence by its words
    sentence_Scores = Calculate_Sentence_Scores(sentences, frequency_table)

    #getting the threshold
    threshold = Calculate_Average_Score(sentence_Scores)

    #producing the summary
    article_Summary = Get_Article_Summary(sentences, sentence_Scores, 1.5 * threshold)

    return article_Summary




if __name__ == '__main__':
    summary_results = _run_article_summary(article_content)
    print("Article Contents: " + article_content[:100]);
    print("\n")
    print(summary_results)