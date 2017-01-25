# Copyright 2016 Rackspace
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import testtools

from syntribos.signal import SignalHolder
from syntribos.signal import SynSignal


class SynSignalUnittest(testtools.TestCase):

    def test_empty_signal(self):
        """Creates empty signal, checks for default values."""
        s = SynSignal()
        self.assertEqual("", s.text)
        self.assertEqual("", s.slug)
        self.assertEqual(0, s.strength)
        self.assertEqual([], s.tags)
        self.assertEqual({}, s.data)

    def test_signal_repr(self):
        """Creates signal w/ slug, asserts that str(signal) is the slug."""
        s = SynSignal(slug="TEST_SIGNAL")
        self.assertEqual("TEST_SIGNAL", str(s))

    def test_match_slug(self):
        """Creates signal w/ slug, asserts that it matches that slug."""
        s = SynSignal(slug="TEST_SIGNAL")
        self.assertTrue(s.matches_slug("TEST_SIGNAL"))

    def test_match_slug_fuzzy(self):
        """Creates signal w/ slug, asserts that it fuzzy-matches that slug."""
        s = SynSignal(slug="TEST_SIGNAL_LONG")
        self.assertTrue(s.matches_slug("TEST_SIGNAL"))

    def test_match_tag(self):
        """Creates signal w/ tag, asserts that it matches that tag."""
        s = SynSignal(tags=["TEST_TAG"])
        self.assertTrue(s.matches_tag("TEST_TAG"))

    def test_match_tag_fuzzy(self):
        """Creates signal w/ tag, asserts that it fuzzy-matches that tag."""
        s = SynSignal(tags=["TEST_TAG_LONG"])
        self.assertTrue(s.matches_tag("TEST_TAG"))

    def test_is_equal(self):
        """Tests 'equality' of two SynSignals."""
        s1 = SynSignal(tags=["TEST_TAG_1"])
        s2 = SynSignal(tags=["TEST_TAG_1"])
        self.assertEqual(s1, s2)
        self.assertEqual(s2, s1)
        s2 = SynSignal(tags=["TEST_TAG_2"])
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s2, s1)
        s2 = SynSignal(tags=["TEST_TAG_2", "TEST_TAG1"])
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s2, s1)


class SignalHolderUnittest(testtools.TestCase):

    @classmethod
    def setUpClass(cls):
        super(SignalHolderUnittest, cls).setUpClass()
        cls.test_signal = SynSignal(
            text="test", slug="TEST_SIGNAL", strength=1, data={"test": "test"},
            tags=["TEST_TAG"])
        cls.test_signal2 = SynSignal(
            text="test2", slug="TEST_SIGNAL2", strength=1,
            data={"test2": "test2"}, tags=["TEST_TAG2"])
        cls.test_signal_0_strength = SynSignal(
            text="test3", slug="TEST_NO_STRENGTH", strength=0,
            data={"test3": "test3"})

    def _assert_same_signal(self, expected, observed):
        for key, item in vars(expected).items():
            self.assertEqual(item, observed.__dict__[key])

    def test_init_one_signal(self):
        """Creates SignalHolder with 1 signal, checks for presence."""
        SH = SignalHolder(self.test_signal)
        self.assertEqual(1, len(SH))
        self._assert_same_signal(self.test_signal, SH[0])

    def test_init_signal_list(self):
        """Creates SignalHolder with list of signals, checks for presence."""
        SH = SignalHolder([self.test_signal, self.test_signal2])
        self.assertEqual(2, len(SH))
        self._assert_same_signal(self.test_signal, SH[0])
        self._assert_same_signal(self.test_signal2, SH[1])

    def test_init_SH(self):
        """Creates SignalHolder with SH of signals, checks for presence."""
        SH = SignalHolder([self.test_signal, self.test_signal2])
        SH2 = SignalHolder(SH)
        self.assertEqual(2, len(SH))
        self.assertEqual(2, len(SH2))
        self._assert_same_signal(self.test_signal, SH2[0])
        self._assert_same_signal(self.test_signal2, SH2[1])

    def test_register_one_signal(self):
        """Creates empty SH, registers 1 signal, checks for presence."""
        SH = SignalHolder()
        SH.register(self.test_signal)
        self.assertEqual(1, len(SH))
        self._assert_same_signal(self.test_signal, SH[0])

    def test_register_signal_list(self):
        """Creates empty SH, registers signal list, checks for presence."""
        SH = SignalHolder()
        SH.register([self.test_signal, self.test_signal2])
        self.assertEqual(2, len(SH))
        self._assert_same_signal(self.test_signal, SH[0])
        self._assert_same_signal(self.test_signal2, SH[1])

    def test_register_SH(self):
        """Creates empty SH, registers SH w/ signals, checks for presence."""
        SH = SignalHolder([self.test_signal, self.test_signal2])
        SH2 = SignalHolder()
        SH2.register(SH)
        self.assertEqual(2, len(SH2))
        self._assert_same_signal(self.test_signal, SH2[0])
        self._assert_same_signal(self.test_signal2, SH2[1])

    def test_register_duplicate_signal(self):
        """Creates empty SH, tries registering dupe signal."""
        SH = SignalHolder()
        SH.register(self.test_signal)
        SH.register(self.test_signal)
        self.assertEqual(1, len(SH))
        self._assert_same_signal(self.test_signal, SH[0])

    def test_register_0_strength_signal(self):
        """Attempts to register a signal w/ strength = 0."""
        SH = SignalHolder()
        SH.register(self.test_signal_0_strength)
        self.assertEqual(0, len(SH))

    def test_contains_slug(self):
        """Creates SH with a signal, checks 'contains' idiom for slugs."""
        SH = SignalHolder(self.test_signal)
        self.assertEqual(1, len(SH))
        self.assertIn(self.test_signal.slug, SH)

    def test_contains_tag(self):
        """Creates SH with a signal, checks 'contains' idiom for tags."""
        SH = SignalHolder(self.test_signal)
        self.assertEqual(len(SH), 1)
        self.assertIn(self.test_signal.slug, SH)

    def test_matching(self):
        """Creates SH with signal, attempts to retrieve w/ search."""
        SH = SignalHolder(self.test_signal)
        matching = SH.find(slugs=self.test_signal.slug)
        self.assertIsInstance(matching, SignalHolder)
        self.assertEqual(1, len(matching))
        self._assert_same_signal(self.test_signal, matching[0])

    def test_SH_repr(self):
        """Creates a SH with signal, checks __repr__ value."""
        SH = SignalHolder(self.test_signal)
        self.assertEqual(1, len(SH))
        self.assertEqual('["TEST_SIGNAL"]', str(SH))

        SH.register(self.test_signal2)
        self.assertEqual(2, len(SH))
        self.assertEqual('["TEST_SIGNAL", "TEST_SIGNAL2"]', str(SH))

    def test_is_equal(self):
        """Tests 'equality' of two SignalHolders."""
        SH1 = SignalHolder(self.test_signal)
        SH2 = SignalHolder(self.test_signal)
        self.assertEqual(SH1, SH2)
        self.assertEqual(SH1, SH2)
        SH2 = SignalHolder(self.test_signal2)
        self.assertNotEqual(SH1, SH2)
        self.assertNotEqual(SH2, SH1)

    def test_compare(self):
        """Tests 'compare' method to see if two SignalHolders differ."""
        SH1 = SignalHolder(self.test_signal)
        SH2 = SignalHolder(self.test_signal)
        data = {"is_diff": False,
                "sh1_len": 1,
                "sh2_len": 1,
                "sh1_not_in_sh2": SignalHolder(),
                "sh2_not_in_sh1": SignalHolder()}
        self.assertEqual(data, SH1.compare(SH2))
        SH2 = SignalHolder(self.test_signal2)
        self.assertNotEqual(data, SH1.compare(SH2))
