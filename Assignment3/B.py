import A
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn import neighbors
import nltk
import collections
import sys

# You might change the window size
window_size = 15


def normalize_tokens(tokens, language):
    """Remove punctuation, apply stemming."""
    try:
        stopwords = set(nltk.corpus.stopwords.words(language))
    except IOError:
        stopwords = {}
    return [t for t in tokens if t.isalnum() and t not in stopwords]


# B.1.a,b,c,d
def extract_features(data, language):
    '''
    :param data: list of instances for a given lexelt with the following structure:
        {
			[(instance_id, left_context, head, right_context, sense_id), ...]
        }
    :return: features: A dictionary with the following structure
             { instance_id: {f1:count, f2:count,...}
            ...
            }
            labels: A dictionary with the following structure
            { instance_id : sense_id }
    '''
    features = {}
    labels = {}
    all_words = collections.Counter()
    if language == 'catalan':
        stemmer = nltk.stem.lancaster.LancasterStemmer()
    else:
        stemmer = nltk.stem.snowball.SnowballStemmer(language)
    # tagger = nltk.tag.perceptron.PerceptronTagger()

    pos_window = 2

    # implement your code here

    # Collect and count all the surrounding words
    for (instance_id, left_context, head, right_context, sense_id) in data:
        left_tokens = [stemmer.stem(t) for t in
                       normalize_tokens(nltk.word_tokenize(left_context.lower()), language)][-window_size:]

        right_tokens = [stemmer.stem(t) for t in
                        normalize_tokens(nltk.word_tokenize(right_context.lower()), language)][:window_size]
        all_words.update(left_tokens + right_tokens)
        labels[instance_id] = sense_id

    # Add features.
    for (instance_id, left_context, head, right_context, sense_id) in data:
        features[instance_id] = {}

        left_tokens = normalize_tokens(nltk.word_tokenize(left_context.lower()), language)
        right_tokens = normalize_tokens(nltk.word_tokenize(right_context.lower()), language)

        # Feature 1: POS of 4 neighbors.
        # left neighbors

        # for i in xrange(1, pos_window + 1):
        #     key = 'POS-{}'.format(i)
        #     for t in nltk.tag.mapping._UNIVERSAL_TAGS:
        #         features[instance_id]['{}-{}'.format(key, t)] = 0
        #
        #     try:
        #         tag = nltk.tag._pos_tag(left_tokens, None, tagger)[-i][1]
        #         features[instance_id]['{}-{}'.format(key, tag)] = 1
        #     except IndexError:
        #         features[instance_id][key] = 0
        # # right neighbors
        # for i in xrange(pos_window):
        #     key = 'POS-{}'.format(i)
        #     for t in nltk.tag.mapping._UNIVERSAL_TAGS:
        #         features[instance_id]['{}-{}'.format(key, t)] = 0
        #
        #     try:
        #         tag = nltk.tag._pos_tag(left_tokens, None, tagger)[i][1]
        #         features[instance_id]['{}-{}'.format(key, tag)] = 1
        #     except IndexError:
        #         features[instance_id][key] = 0

        left_tokens_stemmed = [stemmer.stem(t) for t in left_tokens]
        right_tokens_stemmed = [stemmer.stem(t) for t in right_tokens]
        tokens = left_tokens_stemmed + right_tokens_stemmed
        # Feature 2: add all words as features.
        for w in all_words:
            features[instance_id][w] = tokens.count(w)

    return features, labels


# implemented for you
def vectorize(train_features,test_features):
    '''
    convert set of features to vector representation
    :param train_features: A dictionary with the following structure
             { instance_id: {f1:count, f2:count,...}
            ...
            }
    :param test_features: A dictionary with the following structure
             { instance_id: {f1:count, f2:count,...}
            ...
            }
    :return: X_train: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
            X_test: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
    '''
    X_train = {}
    X_test = {}

    vec = DictVectorizer()
    vec.fit(train_features.values())
    for instance_id in train_features:
        X_train[instance_id] = vec.transform(train_features[instance_id]).toarray()[0]

    for instance_id in test_features:
        X_test[instance_id] = vec.transform(test_features[instance_id]).toarray()[0]

    return X_train, X_test

#B.1.e
def feature_selection(X_train,X_test,y_train):
    '''
    Try to select best features using good feature selection methods (chi-square or PMI)
    or simply you can return train, test if you want to select all features
    :param X_train: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
    :param X_test: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
    :param y_train: A dictionary with the following structure
            { instance_id : sense_id }
    :return:
    '''



    # implement your code here

    #return X_train_new, X_test_new
    # or return all feature (no feature selection):
    return X_train, X_test

# B.2
def classify(X_train, X_test, y_train):
    '''
    Train the best classifier on (X_train, and y_train) then predict X_test labels

    :param X_train: A dictionary with the following structure
            { instance_id: [w_1 count, w_2 count, ...],
            ...
            }

    :param X_test: A dictionary with the following structure
            { instance_id: [w_1 count, w_2 count, ...],
            ...
            }

    :param y_train: A dictionary with the following structure
            { instance_id : sense_id }

    :return: results: a list of tuples (instance_id, label) where labels are predicted by the best classifier
    '''

    results = []


    # implement your code here
    svm_results = []
    knn_results = []

    svm_clf = svm.LinearSVC()
    # knn_clf = neighbors.KNeighborsClassifier()

    x_matrix = []
    y_vector = []
    for instance_id, x in X_train.iteritems():
        x_matrix.append(x)
        y_vector.append(y_train[instance_id])

    svm_clf.fit(x_matrix, y_vector)
    # knn_clf.fit(x_matrix, y_vector)

    for instance_id, x in X_test.iteritems():
        svm_results.append((instance_id, svm_clf.predict(x)[0]))
        # knn_results.append((instance_id, knn_clf.predict(x)[0]))

    return svm_results

# run part B
def run(train, test, language, answer):
    results = {}
    l = len(train)
    for i, lexelt in enumerate(train):
        sys.stdout.write('\r{} / {} ({}%)'.format(i, l, int(float(i) / l * 100)))
        sys.stdout.flush()

        train_features, y_train = extract_features(train[lexelt], language)
        test_features, _ = extract_features(test[lexelt], language)

        X_train, X_test = vectorize(train_features,test_features)
        X_train_new, X_test_new = feature_selection(X_train, X_test,y_train)
        results[lexelt] = classify(X_train_new, X_test_new,y_train)

    A.print_results(results, answer)