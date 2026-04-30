class ReplayWindow:
    def __init__(self, size=32):
        self.size = size
        self.window = set()
        self.max_seq = -1

    def check_and_update(self, seq):
        if seq in self.window:
            return False
        if seq > self.max_seq:
            self.max_seq = seq
        self.window.add(seq)
        if len(self.window) > self.size:
            self.window.remove(min(self.window))
        return True