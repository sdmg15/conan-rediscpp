import os
from conans import ConanFile, CMake, tools

class TrantorConan(ConanFile):
    name = "redis-plus-plus"
    version = "1.1.1"
    license = "MIT"
    author = "sewenew"
    url = "https://github.com/sdmg15/conan-redispp"
    homepage = "https://github.com/sewenew/redis-plus-plus"
    description = "Redis client written in C++"
    topics = ("redis", "db", "memory")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    exports_sources = "CMakeLists.txt"

    requires = (
	"hiredis/0.14.0@hiredis/stable"
    )

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        sha256 = "6cd695e5606dfb624467750264edd6bdc6c855fefd1273fb51697620df1cd013"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)


    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_EXAMPLES"] = False
        cmake.definitions["BUILD_CTL"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def _patch(self):
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "add_subdirectory(test)", "")
        
    def build(self):
        self._patch()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
