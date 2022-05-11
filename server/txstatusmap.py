class TransactionStatusMap:
    def __init__(self):
        self.requests = {}
        self.responses = {}

    def add_request(self, address, threshold):
        if threshold < 1:
            return
        if self.requests.get(address, None) is not None:
            return

        responses = self.responses.get(address, None)
        num_responded = len(responses) if responses is not None else 0
        outcome = None
        if num_responded >= threshold:
            outcome = responses[0]["outcome"]
        self.requests[address] = {
            "outcome": outcome,
            "threshold": threshold
        }

    def add_response(self, address, outcome):
        if address not in self.responses:
            self.responses[address] = []
        self.responses[address].append({
            "outcome": outcome
        })

        request = self.requests.get(address, None)
        requested = request is not None
            
        if requested:
            # request["responded"] = True
            request["outcome"] = outcome
            self.requests[address] = request

    def responded(self, address):
        request = self.requests.get(address, None)
        if request is None:
            return False
        threshold = request["threshold"]
        if threshold == 0:
            return False
        responses = self.responses.get(address, None)
        if responses is None:
            return False
        return threshold >= len(responses)

    def outcome(self, address):
        request = self.requests.get(address, None)
        if request is None:
            return False
        return request["outcome"]