from setuptools import setup

setup(name = "qbibformat",
      version = "1.0",
      packages = ["qbibformat"],
      entry_points = {
          "console_scripts" :
          ["qbibformat = qbibformat.__main__:main"]
      },
  )
