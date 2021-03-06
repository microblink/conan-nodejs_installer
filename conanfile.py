#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration


class NodejsInstallerConan(ConanFile):
    name = "nodejs_installer"
    version = "12.14.0"
    description = "nodejs binaries for use in recipes"
    topics = ("conan", "node", "nodejs")
    url = "https://github.com/microblink/conan-nodejs_installer"
    homepage = "https://nodejs.org"
    author = "Bincrafters <bincrafters@gmail.com>, modified by Microblink"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = "nodejs.patch"
    settings = "os_build", "arch_build"
    _build_subfolder = "build_subfolder"

    def configure(self):
        if self.settings.arch_build == "x86" and self.settings.os_build == "Linux":
            raise ConanInvalidConfiguration("Linux x86 is not support by nodejs {}".format(self.version))

    def build(self):
        arch = "x64" if self.settings.arch_build == "x86_64" else "x86"
        if self.settings.os_build == 'Windows':
            platform = "win"
            extension = "zip"
        elif self.settings.os_build == 'Macos':
            platform = "darwin"
            extension = "tar.gz"
        elif self.settings.os_build == 'Linux':
            platform = "linux"
            extension = "tar.xz"
        else:
            raise ConanInvalidConfiguration("Actual OS is not supported.")

        filename = "node-v{}-{}-{}".format(self.version, platform, arch)
        source_url = "{}/dist/v{}/{}.{}".format(self.homepage, self.version, filename, extension)
        if self.settings.os_build == 'Linux':
            tools.download(source_url, "{}.{}".format(filename, extension))
            # run tar xf manually, as tools.unzip fails with this file
            self.output.info("Decompressing {}.{}...".format(filename, extension))
            self.run("tar xf {}.{}".format(filename, extension))
        else:
            tools.get(source_url)
        extracted_dir = filename
        os.rename(extracted_dir, self._build_subfolder)

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._build_subfolder)
        self.copy(pattern="*", src=self._build_subfolder, dst="", keep_path=True, symlinks=True)

    def package_info(self):
        bin_dir = self.package_folder if tools.os_info.is_windows else os.path.join(self.package_folder, "bin")
        self.env_info.PATH.append(bin_dir)
