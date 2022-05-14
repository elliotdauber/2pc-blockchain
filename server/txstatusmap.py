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
        # data = None
        if num_responded >= threshold:
            outcome = responses[0]["outcome"]
            # data = self.concat_data(address)
        self.requests[address] = {
            "outcome": outcome,
            "threshold": threshold,
            # "data": data
        }

    def add_response(self, address, outcome, data):
        if address not in self.responses:
            self.responses[address] = []
        self.responses[address].append({
            "outcome": outcome,
            "data": data
        })

        request = self.requests.get(address, None)
        requested = request is not None
            
        if requested:
            # old_data = request["data"]
            # if old_data is not None:
            #     if old_data != "":
            #         old_data += ";;"
            #     old_data += data

            request["outcome"] = outcome
            # request["data"] = old_data
            self.requests[address] = request

    def concat_data(self, address):
        responses = self.responses.get(address, None)
        if responses is None:
            return ""
        data = ""
        for response in responses:
            if data != "":
                data += ";;"
            data += response["data"]
        return data

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
            return "UNDEFINED"
        return request["outcome"]

    def data(self, address):
        responses = self.responses.get(address, None)
        if responses is None:
            return ""
        data = ""
        for response in responses:
            if data != "":
                data += ";;"
            data += response["data"]
        return data