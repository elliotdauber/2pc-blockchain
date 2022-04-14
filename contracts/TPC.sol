// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
contract TPC {

    enum State{ INIT, VOTING, COMMIT, ABORT }
    uint256[] public _participants;
    uint256[] public _voted;
    uint256 public _timeout;
    State public _state = State.INIT;

    function request(uint256[] memory participants, uint256 timeout) public {
        assert(_state == State.INIT);
        _participants = participants;
        _timeout = timeout;
    }
}