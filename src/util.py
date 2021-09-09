import json
import os
import subprocess
from datetime import datetime

from .constants import dbName, tempDir, updatedFile


class Util:

    def _createTemp(self):
        """ Create a temp directory """
        if not os.path.exists(tempDir) : os.mkdir(tempDir)
        else : self._resetTemp()

    def executeCommand(self, cmd):
        """ Execute a command """
        return subprocess.run(cmd)

    def exportCollection(self, collection):
        """ Export a collection """
        json_file = os.path.join(tempDir, f"{collection}.json")
        print(f"Exporting collection: {collection} to {json_file}")
        cmd = ["mongoexport","--db",dbName,"--collection",collection, "--out", json_file]
        return self.executeCommand(cmd)

    def importCollection(self, collection, json_file):
        """ Import a collectio to the db """
        if not os.path.abspath(json_file): json_file = os.path.join(os.getcwd(), json_file)
        if not os.path.exists(json_file): raise Exception(f"Error: no such file found for {json_file}")

        print(f"Importing collection: {collection} from: {json_file}")
        cmd = ["mongoimport","--db",dbName,"--collection",collection,"--file",json_file,"--upsert"]
        return self.executeCommand(cmd)

    def _resetTemp(self, tmp_path=tempDir):
        """ Reset the temp folder """
        for file in os.listdir(tmp_path):
            loc = os.path.join(tmp_path, file)
            if os.path.isdir(loc):
                self._resetTemp(loc)
                os.rmdir(loc)
            else: os.remove(loc)

    def setLastUpdated(self, updated=datetime.now()):
        """ Update the lastUpdated.json file """
        path = os.path.join(tempDir, updatedFile)
        with open(path, 'a') as file:
            file.write(f"Last updated at {str(updated)}\n")


if __name__ == "__main__":
    pass