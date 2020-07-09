from hypothesis import given, settings

from converter.config import Config
from converter.mapping import MappingSpec
from converter.mapping.base import TransformationEntry

from ..connector.fakes import FakeConnector
from ..helpers import NaNChecker
from ..mapping.fakes import FakeMapping
from .stategies import runners


@given(runner_class=runners())
@settings(deadline=None)
def test_filter_contains_and(runner_class):
    input_data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
        {"a": 5, "b": 6},
        {"a": 7, "b": 8},
    ]

    mapping = FakeMapping(
        "A",
        "B",
        [
            MappingSpec(
                "A",
                "B",
                forward_transform={
                    "c": [
                        TransformationEntry(
                            transformation="a * 2", when="a is 1 and b is 2",
                        )
                    ],
                    "d": [
                        TransformationEntry(
                            transformation="b + 3", when="a is 5 and b is 6",
                        )
                    ],
                },
            )
        ],
    )

    extractor = FakeConnector(data=input_data)
    loader = FakeConnector()

    runner_class(Config()).run(extractor, mapping, loader)

    assert list(loader.data) == [
        {"c": 2, "d": NaNChecker()},
        {"c": NaNChecker(), "d": 9},
    ]


@given(runner_class=runners())
@settings(deadline=None)
def test_filter_contains_or(runner_class):
    input_data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
        {"a": 5, "b": 6},
        {"a": 7, "b": 8},
    ]

    mapping = FakeMapping(
        "A",
        "B",
        [
            MappingSpec(
                "A",
                "B",
                forward_transform={
                    "c": [
                        TransformationEntry(
                            transformation="a * 2", when="a is 1 or a is 5",
                        )
                    ],
                    "d": [
                        TransformationEntry(
                            transformation="b + 3", when="b is 2 or b is 6",
                        )
                    ],
                },
            )
        ],
    )

    extractor = FakeConnector(data=input_data)
    loader = FakeConnector()

    runner_class(Config()).run(extractor, mapping, loader)

    assert list(loader.data) == [
        {"c": 2, "d": 5},
        {"c": 10, "d": 9},
    ]


@given(runner_class=runners())
@settings(deadline=None)
def test_filter_contains_in___lhs_is_lookup_rhs_is_list_of_ints(runner_class):
    input_data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
        {"a": 5, "b": 6},
        {"a": 7, "b": 8},
    ]

    mapping = FakeMapping(
        "A",
        "B",
        [
            MappingSpec(
                "A",
                "B",
                forward_transform={
                    "c": [
                        TransformationEntry(
                            transformation="a * 2", when="a is in [1, 5]",
                        )
                    ],
                    "d": [
                        TransformationEntry(
                            transformation="b + 3", when="b is in [2, 6]",
                        )
                    ],
                },
            )
        ],
    )

    extractor = FakeConnector(data=input_data)
    loader = FakeConnector()

    runner_class(Config()).run(extractor, mapping, loader)

    assert list(loader.data) == [
        {"c": 2, "d": 5},
        {"c": 10, "d": 9},
    ]


@given(runner_class=runners())
@settings(deadline=None)
def test_filter_contains_in___lhs_is_int_rhs_is_list_of_lookups(runner_class):
    input_data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
        {"a": 5, "b": 6},
        {"a": 7, "b": 8},
    ]

    mapping = FakeMapping(
        "A",
        "B",
        [
            MappingSpec(
                "A",
                "B",
                forward_transform={
                    "c": [
                        TransformationEntry(
                            transformation="a * 2", when="1 is in [a, b]",
                        )
                    ],
                    "d": [
                        TransformationEntry(
                            transformation="b + 3", when="6 is in [a, b]",
                        )
                    ],
                },
            )
        ],
    )

    extractor = FakeConnector(data=input_data)
    loader = FakeConnector()

    runner_class(Config()).run(extractor, mapping, loader)

    assert list(loader.data) == [
        {"c": 2, "d": NaNChecker()},
        {"c": NaNChecker(), "d": 9},
    ]


@given(runner_class=runners())
@settings(deadline=None)
def test_filter_contains_in___lhs_is_int_rhs_is_list_of_ints(runner_class):
    input_data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
        {"a": 5, "b": 6},
        {"a": 7, "b": 8},
    ]

    mapping = FakeMapping(
        "A",
        "B",
        [
            MappingSpec(
                "A",
                "B",
                forward_transform={
                    "c": [
                        TransformationEntry(
                            transformation="a * 2", when="1 is in [1, 2]",
                        )
                    ],
                    "d": [
                        TransformationEntry(
                            transformation="b + 3", when="6 is in [1, 2]",
                        )
                    ],
                },
            )
        ],
    )

    extractor = FakeConnector(data=input_data)
    loader = FakeConnector()

    runner_class(Config()).run(extractor, mapping, loader)

    assert list(loader.data) == [
        {"c": 2, "d": NaNChecker()},
        {"c": 6, "d": NaNChecker()},
        {"c": 10, "d": NaNChecker()},
        {"c": 14, "d": NaNChecker()},
    ]


@given(runner_class=runners())
@settings(deadline=None)
def test_filter_contains_in___lhs_is_lookup_rhs_is_list_of_lookups(
    runner_class,
):
    input_data = [
        {"a": 1, "b": 2, "c": 1},
        {"a": 3, "b": 4, "c": 4},
        {"a": 5, "b": 6, "c": 5},
        {"a": 7, "b": 8, "c": 8},
    ]

    mapping = FakeMapping(
        "A",
        "B",
        [
            MappingSpec(
                "A",
                "B",
                forward_transform={
                    "c": [
                        TransformationEntry(
                            transformation="a * 2", when="a is in [b, c]",
                        )
                    ],
                    "d": [
                        TransformationEntry(
                            transformation="b + 3", when="b is in [a, c]",
                        )
                    ],
                },
            )
        ],
    )

    extractor = FakeConnector(data=input_data)
    loader = FakeConnector()

    runner_class(Config()).run(extractor, mapping, loader)

    assert list(loader.data) == [
        {"c": 2, "d": NaNChecker()},
        {"c": NaNChecker(), "d": 7},
        {"c": 10, "d": NaNChecker()},
        {"c": NaNChecker(), "d": 11},
    ]


@given(runner_class=runners())
@settings(deadline=None)
def test_filter_contains_not_in___lhs_is_lookup_rhs_is_list_of_ints(
    runner_class,
):
    input_data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
        {"a": 5, "b": 6},
        {"a": 7, "b": 8},
    ]

    mapping = FakeMapping(
        "A",
        "B",
        [
            MappingSpec(
                "A",
                "B",
                forward_transform={
                    "c": [
                        TransformationEntry(
                            transformation="a * 2", when="a is not in [1, 5]",
                        )
                    ],
                    "d": [
                        TransformationEntry(
                            transformation="b + 3", when="b is not in [2, 6]",
                        )
                    ],
                },
            )
        ],
    )

    extractor = FakeConnector(data=input_data)
    loader = FakeConnector()

    runner_class(Config()).run(extractor, mapping, loader)

    assert list(loader.data) == [
        {"c": 6, "d": 7},
        {"c": 14, "d": 11},
    ]


@given(runner_class=runners())
@settings(deadline=None)
def test_filter_contains_not_in___lhs_is_int_rhs_is_list_of_lookups(
    runner_class,
):
    input_data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
        {"a": 5, "b": 6},
        {"a": 7, "b": 8},
    ]

    mapping = FakeMapping(
        "A",
        "B",
        [
            MappingSpec(
                "A",
                "B",
                forward_transform={
                    "c": [
                        TransformationEntry(
                            transformation="a * 2", when="1 is not in [a, b]",
                        )
                    ],
                    "d": [
                        TransformationEntry(
                            transformation="b + 3", when="6 is not in [a, b]",
                        )
                    ],
                },
            )
        ],
    )

    extractor = FakeConnector(data=input_data)
    loader = FakeConnector()

    runner_class(Config()).run(extractor, mapping, loader)

    assert list(loader.data) == [
        {"c": NaNChecker(), "d": 5},
        {"c": 6, "d": 7},
        {"c": 10, "d": NaNChecker()},
        {"c": 14, "d": 11},
    ]


@given(runner_class=runners())
@settings(deadline=None)
def test_filter_contains_not_in___lhs_is_int_rhs_is_list_of_ints(runner_class):
    input_data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
        {"a": 5, "b": 6},
        {"a": 7, "b": 8},
    ]

    mapping = FakeMapping(
        "A",
        "B",
        [
            MappingSpec(
                "A",
                "B",
                forward_transform={
                    "c": [
                        TransformationEntry(
                            transformation="a * 2", when="1 is not in [1, 2]",
                        )
                    ],
                    "d": [
                        TransformationEntry(
                            transformation="b + 3", when="6 is not in [1, 2]",
                        )
                    ],
                },
            )
        ],
    )

    extractor = FakeConnector(data=input_data)
    loader = FakeConnector()

    runner_class(Config()).run(extractor, mapping, loader)

    assert list(loader.data) == [
        {"c": NaNChecker(), "d": 5},
        {"c": NaNChecker(), "d": 7},
        {"c": NaNChecker(), "d": 9},
        {"c": NaNChecker(), "d": 11},
    ]


@given(runner_class=runners())
@settings(deadline=None)
def test_filter_contains_not_in___lhs_is_lookup_rhs_is_list_of_lookups(
    runner_class,
):
    input_data = [
        {"a": 1, "b": 2, "c": 1},
        {"a": 3, "b": 4, "c": 4},
        {"a": 5, "b": 6, "c": 5},
        {"a": 7, "b": 8, "c": 8},
    ]

    mapping = FakeMapping(
        "A",
        "B",
        [
            MappingSpec(
                "A",
                "B",
                forward_transform={
                    "c": [
                        TransformationEntry(
                            transformation="a * 2", when="a is not in [b, c]",
                        )
                    ],
                    "d": [
                        TransformationEntry(
                            transformation="b + 3", when="b is not in [a, c]",
                        )
                    ],
                },
            )
        ],
    )

    extractor = FakeConnector(data=input_data)
    loader = FakeConnector()

    runner_class(Config()).run(extractor, mapping, loader)

    assert list(loader.data) == [
        {"c": NaNChecker(), "d": 5},
        {"c": 6, "d": NaNChecker()},
        {"c": NaNChecker(), "d": 9},
        {"c": 14, "d": NaNChecker()},
    ]


@given(runner_class=runners())
@settings(deadline=None)
def test_filter_contains_not___value_is_lookup(runner_class):
    input_data = [
        {"a": 1, "b": 2, "c": 1},
        {"a": 3, "b": 4, "c": 4},
        {"a": 5, "b": 6, "c": 5},
        {"a": 7, "b": 8, "c": 8},
    ]

    mapping = FakeMapping(
        "A",
        "B",
        [
            MappingSpec(
                "A",
                "B",
                forward_transform={
                    "c": [
                        TransformationEntry(
                            transformation="a * 2", when="not (a is 1)",
                        )
                    ],
                    "d": [
                        TransformationEntry(
                            transformation="b + 3", when="not (b is 6)",
                        )
                    ],
                },
            )
        ],
    )

    extractor = FakeConnector(data=input_data)
    loader = FakeConnector()

    runner_class(Config()).run(extractor, mapping, loader)

    assert list(loader.data) == [
        {"c": NaNChecker(), "d": 5},
        {"c": 6, "d": 7},
        {"c": 10, "d": NaNChecker()},
        {"c": 14, "d": 11},
    ]


@given(runner_class=runners())
@settings(deadline=None)
def test_filter_contains_not___value_is_bool(runner_class):
    input_data = [
        {"a": 1, "b": 2, "c": 1},
        {"a": 3, "b": 4, "c": 4},
        {"a": 5, "b": 6, "c": 5},
        {"a": 7, "b": 8, "c": 8},
    ]

    mapping = FakeMapping(
        "A",
        "B",
        [
            MappingSpec(
                "A",
                "B",
                forward_transform={
                    "c": [
                        TransformationEntry(
                            transformation="a * 2", when="not False",
                        )
                    ],
                    "d": [
                        TransformationEntry(
                            transformation="b + 3", when="not True",
                        )
                    ],
                },
            )
        ],
    )

    extractor = FakeConnector(data=input_data)
    loader = FakeConnector()

    runner_class(Config()).run(extractor, mapping, loader)

    assert list(loader.data) == [
        {"c": 2, "d": NaNChecker()},
        {"c": 6, "d": NaNChecker()},
        {"c": 10, "d": NaNChecker()},
        {"c": 14, "d": NaNChecker()},
    ]