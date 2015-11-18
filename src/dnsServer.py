from application import Application
from threading import Thread
from queue import LifoQueue, Empty, Full

class DnsServer(Application):

    def __init__(self, name, host):
        Application.__init__(self, name, host);
        self.thread = Thread(target=self.runThread, daemon=True)
        self.thread.start()

    def runThread(self):
        """Host's infinite thread loop. Receives and sends messages
           to other hosts."""
        print("Application ", self.name, " on host ", self.getHost().name)
        while(True):
            try:
                command = self.getHost().simQueue.get_nowait()
                self.getHost().processCommand(command)
                self.getHost().simQueue.task_done()
            except Empty:
                pass

            try:
                packet = self.getHost().netQueue.get_nowait()
                self.getHost().processPacket(packet)
                self.getHost().netQueue.task_done()
            except Empty:
                pass
