import spacy
import sklearn.preprocessing
from textacy.vsm import Vectorizer
from django.core.management.base import BaseCommand
from newcomers_guide.read_data import read_task_data
from newcomers_guide.parse_data import parse_task_files
from search.models import TaskSimilarityScores
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Compute text similarity scores between Newcomers\' Guide content and service provider descriptions, store them in the database'

    def add_arguments(self, parser):
        parser.add_argument('path',
                            metavar='path',
                            help='path to root of Newcomers Guide folder structure')

    def handle(self, *args, **options):
        root_folder = options['path']
        ids, docs = read_task_descriptions(root_folder)
        cosine_doc_similarities = compute_similarities(docs)
        save_task_similarities(ids, cosine_doc_similarities)


def read_task_descriptions(root_folder):
    task_data = read_task_data(root_folder)
    tasks = parse_task_files(task_data)
    return to_ids_and_descriptions(tasks)


def to_ids_and_descriptions(tasks):
    ids = []
    descriptions = []
    for task_id, task in tasks['taskMap'].items():
        ids.append(slugify(task_id))
        english_description = task_id + ' ' + task['description']['en']
        descriptions.append(english_description)
    return (ids, descriptions)


def compute_similarities(docs):
    nlp = spacy.load('en')
    spacy_docs = [nlp(doc) for doc in docs]
    tokenized_docs = ([tok.lemma_ for tok in doc] for doc in spacy_docs)
    vectorizer = Vectorizer(tf_type='linear', apply_idf=True, idf_type='smooth', apply_dl=False)
    term_matrix = vectorizer.fit_transform(tokenized_docs)
    return compute_cosine_doc_similarities(term_matrix)


def compute_cosine_doc_similarities(matrix):
    normalized_matrix = sklearn.preprocessing.normalize(matrix, axis=1)
    return normalized_matrix * normalized_matrix.T


def save_task_similarities(ids, similarities):
    TaskSimilarityScores.objects.all().delete()
    for i in range(len(ids)):
        for j in range(i):
            first_id = ids[i]
            second_id = ids[j]
            score = similarities[i, j]
            record = TaskSimilarityScores(first_task_id=first_id,
                                          second_task_id=second_id,
                                          similarity_score=score)
            record.save()
