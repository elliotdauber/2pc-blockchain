// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
contract TPC {
    struct Set {
        uint32[] values;
        mapping(uint32 => bool) is_in;
    }

    //enum State{ INIT, VOTING, COMMIT, ABORT, TIMEOUT }
    uint32 _num_nodes;
    uint256 public _timeout;
    uint256 public _timeout_len;
    string _state = "INIT";
    Set _voters;
    string _data = "";
    bool _data_set = false;

    function set_contains(Set storage s, uint32 a) private view returns (bool) {
        return s.is_in[a];
    }

    function set_add(Set storage s, uint32 a) private {
        if (!set_contains(s, a)) {
            s.values.push(a);
            s.is_in[a] = true;
        }
    }

    function set_size(Set storage s) private view returns (uint256) {
        return s.values.length;
    }

    //TODO finish
    function request(uint32 num_nodes, uint256 timeout) public {
        _timeout_len = timeout;
        _timeout = block.timestamp + timeout;
        _num_nodes = num_nodes;
        _state = "VOTING";
    }

    //TODO finish

    function voter(uint32 vote, uint32 nodeid) public {
        if (
            keccak256(abi.encodePacked(_state)) !=
            keccak256(abi.encodePacked("VOTING")) ||
            set_size(_voters) == _num_nodes
        ) {
            return;
        }
        if (block.timestamp > _timeout) {
            _state = "TIMEOUT";
        } else if (vote == 0) {
            _state = "ABORT";
        } else {
            set_add(_voters, nodeid);
            if (set_size(_voters) == _num_nodes) {
                _state = "COMMIT";
            }
        }
    }

    function set_data(string calldata data) public {
        if (_data_set) {
            _data = string(abi.encodePacked(_data, ";;"));
        }
        _data = string(abi.encodePacked(_data, data));
        _data_set = true;
    }

    function verdict() public {
        if (
            keccak256(abi.encodePacked(_state)) ==
            keccak256(abi.encodePacked("VOTING")) &&
            block.timestamp > _timeout
        ) {
            _state = "TIMEOUT";
        }
    }

    function getState() public view returns (string memory) {
        return _state;
    }

    function getData() public view returns (string memory) {
        return _data;
    }

    function getTimeout() public view returns (uint256) {
        return _timeout_len;
    }
}
