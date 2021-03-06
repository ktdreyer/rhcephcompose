import logging
import os
import re
import requests
from shutil import copy

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('cephcomps')

class PackageArtifact(object):
    """ Artifact from a Chacra build. Base class. """
    def __init__(self, url):
        self.url = url

    @property
    def filename(self):
        """ Return the filename, eg ruby-rkerberos_0.1.3-2trusty_amd64.deb """
        return os.path.basename(self.url)

    def download(self, cache_dir, dest_dir=None):
        """ Download self.url to cache_dir, then copy to dest_dir. """
        # Calculate the download destination in the cache_dir:
        cache_dest = os.path.join(cache_dir, self.filename)
        # Do we have a cached copy of this file, or not?
        if os.path.isfile(cache_dest):
            log.info('%s already in %s, skipping download' % (self.filename, cache_dir))
        else:
            log.info('Caching %s in %s' % (self.url, cache_dir))
            r = requests.get(self.url, stream=True)
            r.raise_for_status()
            with open(cache_dest, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        if dest_dir is not None:
            copy(cache_dest, dest_dir)


class SourceArtifact(PackageArtifact):
    """ Source Artifact from chacra. """
    def __init__(self, url):
        super(SourceArtifact, self).__init__(url=url)


class BinaryArtifact(PackageArtifact):
    """ Binary Artifact from chacra (ie ".deb" file). """

    # Regex to parse the name and version of this binary.
    name_version_re = re.compile('^([^_]+)_([^_]+)')

    def __init__(self, url):
        super(BinaryArtifact, self).__init__(url=url)

    @property
    def name(self):
        """ Return the name of a Debian build, eg "ruby-rkerberos" or "ceph".
        Corresponds to "project_name" in Chacra. """
        return self.name_version_re.search(self.filename).group(1)
