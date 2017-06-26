import copy

from typing import List, Tuple, Union
from collections import namedtuple

from django.db.models.query_utils import PathInfo
from django.contrib.postgres.fields import HStoreField as DjangoHStoreField

# Opaque object for faking a field class that refers to a single key
# within a HStoreField... This is used to include in PathInfo objects
# which normally describe joins, but in this case we are "joining"
# on a hstore key rather than another table.
HStoreFieldKey = namedtuple('HStoreFieldKey', 'model field key is_relation')


class HStoreField(DjangoHStoreField):
    """Improved version of Django's :see:HStoreField that
    adds support for database-level constraints.

    Notes:
        - For the implementation of uniqueness, see the
          custom database back-end.
    """

    def __init__(self, *args,
                 uniqueness: List[Union[str, Tuple[str, ...]]]=None,
                 required: List[str]=None, **kwargs):
        """Initializes a new instance of :see:HStoreField."""

        super(HStoreField, self).__init__(*args, **kwargs)

        self.uniqueness = uniqueness
        self.required = required

    def deconstruct(self):
        """Gets the values to pass to :see:__init__ when
        re-creating this object."""

        name, path, args, kwargs = super(
            HStoreField, self).deconstruct()

        kwargs['uniqueness'] = self.uniqueness or []
        kwargs['required'] = self.required or []

        return name, path, args, kwargs

    def get_path_info(self):
        """Gets the information about join-able fields in this
        field.

        This method is typically implemented by relational field
        which point to another model. This method would return
        the list of fields in the foreign model.

        HStoreField is not a relational field, but attempts to
        simulate one in this case by "imagining" each hstore key
        is a field in another model. This allows "joining" on
        individual hstore keys.

        In simple terms: this makes `title__en` in .values() work.
        """

        def get_field(name):
            return HStoreFieldKey(
                model=self.model,
                field=self,
                key=name,
                is_relation=False
            )

        # make a copy of the meta object here so we can monkey patch
        # the get_field method, rather than messing around in the actual object
        opts = copy.copy(self.model._meta)
        opts.get_field = get_field

        # return a somehwat mocket PathInfo object that actualy points to itself
        # rather than to another model (as is it would if this was a foreign key)
        return [PathInfo(opts, opts, [], self, False, True)]
