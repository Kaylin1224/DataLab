import json

import datalabs
from datalabs import get_task, TaskType
from datalabs.features import Sequence, Value

_DESCRIPTION = """\
Bagel is a meta-evaluation datasets in the data-to-text domain. It provides 
information about restaurants. Each sample in it consists of one meaning 
representation, multiple references, and utterances generated by different 
systems.
"""

_CITATION = """\
@inproceedings{mairesse-etal-2010-phrase,
    title = "Phrase-Based Statistical Language Generation Using Graphical Models and Active Learning",
    author = "Mairesse, Fran{\c{c}}ois  and
      Ga{\v{s}}i{\'c}, Milica  and
      Jur{\v{c}}{\'\i}{\v{c}}ek, Filip  and
      Keizer, Simon  and
      Thomson, Blaise  and
      Yu, Kai  and
      Young, Steve",
    booktitle = "Proceedings of the 48th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2010",
    address = "Uppsala, Sweden",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P10-1157",
    pages = "1552--1561",
}
"""

_TEST_DOWNLOAD_URL = "https://datalab-hub.s3.amazonaws.com/meval/bagel/test.jsonl"


class MevalBAGELConfig(datalabs.BuilderConfig):


    def __init__(
        self,
        evaluation_aspect = None,
        **kwargs
    ):
        super(MevalBAGELConfig, self).__init__(**kwargs)
        self.evaluation_aspect = evaluation_aspect

class MevalBAGEL(datalabs.GeneratorBasedBuilder):

    evaluation_aspects = [
        "informativeness",
        "naturalness",
        "quality"
    ]

    BUILDER_CONFIGS = [MevalBAGELConfig(
        name=aspect,
        version=datalabs.Version("1.0.0"),
        evaluation_aspect=aspect
    ) for aspect in evaluation_aspects]



    def _info(self):
        features = datalabs.Features(
            {
                "source": Value("string"),
                "references": Sequence(Value("string")),
                "hypotheses": Sequence({
                    "system_name": Value("string"),
                    "hypothesis": Value("string")
                }
                ),
                "scores": Sequence(Value("float")),
            }
        )
        return datalabs.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage="https://github.com/jeknov/EMNLP_17_submission",
            citation=_CITATION,
            languages=["en"],
            task_templates=[
                get_task(TaskType.meta_evaluation_nlg)(
                    source_column="source",
                    hypotheses_column="hypothesis",
                    references_column="references",
                    scores_column = "scores",
                )
            ]
        )

    def _split_generators(self, dl_manager):
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            datalabs.SplitGenerator(
                name=datalabs.Split.TEST, gen_kwargs={"filepath": test_path}
            ),
        ]

    def _generate_examples(self, filepath):
        """ Generate BAGEL examples."""
        with open(filepath, "r", encoding="utf-8") as f:
            for id_, line in enumerate(f.readlines()):
                line = line.strip()
                line = json.loads(line)
                source, hypothesis, references, scores = line["source"], \
                                                         line["hypothesis"],\
                                                         line["references"],\
                                                         line["scores"]

                yield id_, {
                    "source": source,
                    "hypotheses": [{
                        "system_name": "Unknown",
                        "hypothesis": hypothesis,
                    }],
                    "scores": [scores[self.config.name]],
                    "references": references,
                }
