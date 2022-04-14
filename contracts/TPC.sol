// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
contract TPC {

    enum State{ INIT, VOTING, COMMIT, ABORT }
    address[] public _participants;
    address[] public _voted;
    uint256 public _timeout;
    State public _state = State.INIT;

    //TODO finish
    function request(address[] memory participants, uint256 timeout) public {
        assert(_state == State.INIT);
        _participants = participants;
        _timeout = timeout;
        _state = State.VOTING;
    }

    //TODO finish
    function voter(int vote) public {
        assert(_state == State.VOTING);
        assert(vote == 1);
        _voted.push(msg.sender);
        //if _voted == _participants
        _state = State.COMMIT;
    }

    function verdict() public {
        //TODO
    }
}