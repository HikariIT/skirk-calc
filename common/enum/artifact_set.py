from enum import Enum


class ArtifactSet(Enum):
    GOLDEN_TROUPE = 1
    MARECHAUSSE_HUNTER = 2
    SCROLL_OF_THE_HERO_OF_CINDER_CITY = 3
    FINALE_OF_THE_DEEP_GALLERIES = 4
    NO_ARTIFACT_SET = 5

    @staticmethod
    def get_from_name(name: str) -> 'ArtifactSet':
        for artifact_set in ArtifactSet:
            if artifact_set.name == name:
                return artifact_set
        return ArtifactSet.NO_ARTIFACT_SET