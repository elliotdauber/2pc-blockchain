// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
contract TPC {

    enum State{ INIT, VOTING, COMMIT, ABORT }
    mapping (uint32 => uint32) public _votes;
    uint32 _num_nodes;
    uint256 public _timeout;
    State public _state = State.INIT;

    //TODO finish
    function request(uint32 num_nodes, uint256 timeout) public {
        assert(_state == State.INIT);
        _timeout = timeout;
        _num_nodes = num_nodes;
        _state = State.VOTING;
    }

    //TODO finish
    function voter(uint32 vote, uint32 nodeid) public {
        //assert(_state == State.VOTING);
        //assert(vote == 1);
        //_votes[nodeid] = vote;
        //_if _voted == _participants
        _state = State.COMMIT;
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