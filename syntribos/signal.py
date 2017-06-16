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
import six

from syntribos._i18n import _


class SignalHolder(object):
    """SignalHolder represents a 'set' of SynSignals.

    :ivar list signals: Collection of :class:`SynSignal`
    :ivar list all_slugs: Collection of slugs in `signals` for fast search
    """

    def __init__(self, signals=None):
        """The SignalHolder can be initialized with a set of signals

        :param signals: Collection of signals (added with `self.register()`)
        :type signals: :class:`SynSignal` OR :class:`SignalHolder` OR `list`
        """
        self.signals = []
        self.all_slugs = []

        if signals is not None:
            self.register(signals)

    def __getitem__(self, key):
        return self.signals[key]

    def __setitem__(self, key, value):
        if not isinstance(value, SynSignal):
            raise TypeError()

        if value.strength == 0:
            return

        if value.slug not in self.all_slugs:
            self.signals[key] = value
            self.all_slugs[key] = value.slug

    def __delitem__(self, key):
        del self.signals[key]
        # Indices for self.signals/self.all_slugs should be the same
        del self.all_slugs[key]

    def __repr__(self):
        return '["' + '", "'.join([sig.slug for sig in self.signals]) + '"]'

    def __len__(self):
        return len(self.signals)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        s1_has_s2 = all([sig in self.signals for sig in other.signals])
        s2_has_s1 = all([sig in other.signals for sig in self.signals])
        return s1_has_s2 and s2_has_s1

    def __ne__(self, other):
        return not self.__eq__(other)

    def __contains__(self, item):
        """This is used to search for signals in the 'if __ in __' pattern."""
        if not isinstance(item, SynSignal) and not isinstance(
                item, six.string_types):
            raise TypeError()

        if isinstance(item, six.string_types):
            # We are searching for either a tag or a slug
            for signal in self.signals:
                if signal.matches_slug(item):
                    return True
                if signal.matches_tag(item):
                    return True
            return False
        else:
            # We are searching for a signal by its slug (unique ID)
            return item.slug in self.all_slugs

    def register(self, signals):
        """Add a signal/list of signals to the SignalHolder

        Maintains a set (won't add signal if its slug is in `self.all_slugs`)

        :param signals: A single SynSignal, or a collection of them
        :type signals: :class:`SynSignal` OR list OR :class:`SynHolder`
        """
        if signals is None:
            return

        if isinstance(signals, SynSignal):
            if self._is_dead(signals):
                return
            elif self._is_duplicate(signals):
                return
            self.signals.append(signals)
            self.all_slugs.append(signals.slug)

        elif isinstance(signals, list) or isinstance(signals, SignalHolder):
            for signal in signals:
                self.register(signal)

        else:
            raise TypeError()

    def find(self, slugs=None, tags=None):
        """Get the signals that are matched by `slugs` and/or `tags`

        :param list slugs: A `list` of slugs to search for
        :param list tags: A `list` of tags to search for
        :rtype: class
        :returns: A :class:`SignalHolder` of matched :class:`SynSignal`
        """
        bad_signals = SignalHolder()

        if slugs:
            for bad_slug in slugs:
                bad_signals.register([
                    sig for sig in self.signals if sig.matches_slug(bad_slug)
                ])
        if tags:
            for bad_tag in tags:
                bad_signals.register(
                    [sig for sig in self.signals if sig.matches_tag(bad_tag)])

        return bad_signals

    def _is_dead(self, signal):
        return signal is None or signal.strength == 0

    def _is_duplicate(self, signal):
        return signal.slug in self.all_slugs

    def ran_check(self, check_name):
        for signal in self.signals:
            if signal.check_name == check_name:
                return True

    def compare(self, other):
        """Returns a dict with details of diff between 2 SignalHolders.

        :param: signal_holder1
        :ptype: :class:  Syntribos.signal.SignalHolder
        :param: signal_holder2
        :ptype: :class:  Syntribos.signal.SignalHolder
        :returns: data
        :rtype: :dict:
        """
        data = {
            "is_diff": False,
            "sh1_len": len(self),
            "sh2_len": len(other),
            "sh1_not_in_sh2": SignalHolder(),
            "sh2_not_in_sh1": SignalHolder()
        }
        if self == other:
            return data
        for signal in self.signals:
            if signal not in other:
                data["is_diff"] = True
                data["sh1_not_in_sh2"].register(signal)
        for signal in other.signals:
            if signal not in self:
                data["is_diff"] = True
                data["sh2_not_in_sh1"].register(signal)
        return data


class SynSignal(object):
    """SynSignal represents a piece of information raised by a 'check'

    :ivar str text: A message describing the signal
    :ivar str slug: A unique slug that identifies the signal
    :ivar float strength: A number from 0 to 1 representing confidence
    :ivar list tags: Collection of tags associated with the signal
    :ivar dict data: Information about the results of the check
    """

    def __init__(self,
                 text="",
                 slug="",
                 strength=0.0,
                 tags=None,
                 data=None,
                 check_name=None):
        self.text = text if text else ""
        self.slug = slug if slug else ""
        self.check_name = check_name if check_name else ""

        if self.__dict__.get("strength", None):
            self.strength = self.strength
        else:
            self.strength = strength
        self.tags = tags if tags else []
        self.data = data if data else {}

    def __repr__(self):
        return self.slug

    def __eq__(self, other):
        same_tags = self.tags == other.tags
        same_slug = self.slug == other.slug
        same_check_name = self.check_name == other.check_name
        return same_tags and same_slug and same_check_name

    def __ne__(self, other):
        return not self.__eq__(other)

    def matches_tag(self, tag):
        """Checks if a Signal has a given tag

        :param str tag: Tag to search for
        :rtype: bool
        :returns: True if fuzzy match, else False
        """
        for t in self.tags:
            if tag in t:
                return True
        return False

    def matches_slug(self, slug):
        """Checks if a Signal has a given slug

        :param str slug: Slug to search for
        :rtype: bool
        :returns: True if fuzzy match, else False
        """
        slug = slug.upper()
        return slug in self.slug


def from_generic_exception(exception):
    """Return a SynSignal from a generic Exception

    :param exception: A generic Exception that can't be identified
    :type exception: Exception
    :rtype: :class:`SynSignal`
    :returns: A signal describing the exception
    """
    if not isinstance(exception, Exception):
        raise Exception(_("This function accepts only Exception objects"))

    exc_text = str(exception)
    text = _("This request raised an exception: '%s'") % exc_text
    data = {
        _("exception_name"): exception.__class__.__name__,
        _("exception_text"): exc_text,
        _("exception"): exception
    }
    slug = "GENERIC_EXCEPTION_{name}".format(
        name=data["exception_name"].upper())
    tags = ["EXCEPTION_RAISED"]

    return SynSignal(text=text, slug=slug, strength=1.0, tags=tags, data=data)
