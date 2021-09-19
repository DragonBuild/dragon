from hummingbird.loader import DragonMakeLoader
from hummingbird.logosdriver import LogosDriver
from hummingbird.generator import NinjaFileGenerator

if __name__ == "__main__":
    
    loader = DragonMakeLoader()
    logos_driver = LogosDriver(loader.modules[0].config)

    generator = NinjaFileGenerator(logos_driver)
    generator.generate('build.ninja')