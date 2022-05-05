// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
contract TPC {
    struct Set {
        uint32[] values;
        mapping (uint32 => bool) is_in;
    }


    enum State{ INIT, VOTING, COMMIT, ABORT }
    uint32 _num_nodes;
    uint256 public _timeout;
    State public _state = State.INIT;
    Set _voters;

    function set_contains(Set storage s, uint32 a) private returns (bool) {
        return s.is_in[a];
    }

    function set_add(Set storage s, uint32 a) private {
        if (!set_contains(s, a)) {
            s.values.push(a);
            s.is_in[a] = true;
        }
    }

    function set_size(Set storage s) private returns (uint) {
        return s.values.length;
    }

    //TODO finish
    function request(uint32 num_nodes, uint256 timeout) public {
        assert(_state == State.INIT);
        _timeout = timeout;
        _num_nodes = num_nodes;
        _state = State.VOTING;
    }

    //TODO finish
    function voter(uint32 vote, uint32 nodeid) public {
        assert(_state == State.VOTING);
        if (vote == 0) {
            _state = State.ABORT;
            return;
        }
        set_add(_voters, nodeid);
        if (set_size(_voters) == _num_nodes) {
            _state = State.COMMIT;
        }
    }

    function verdict() public {
        //TODO
    }

    function getState() public view returns (string memory) {
        if (_state == State.INIT) {return "INIT";}
        if (_state == State.VOTING) {return "VOTING";}
        if (_state == State.COMMIT) {return "COMMIT";}
        if (_state == State.ABORT) {return "ABORT";}
        return "NONE";
    }
}