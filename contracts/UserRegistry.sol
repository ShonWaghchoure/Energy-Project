// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract UserRegistry {
    enum Role { None, Prosumer, Consumer }

    struct User {
        address addr;
        Role role;
        uint256 reputation; // Scale 0-100, starts at 50
        bool isRegistered;
    }

    mapping(address => User) public users;
    address[] public allUsers;
    address public admin;

    constructor() {
        admin = msg.sender;
    }

    function registerUser(Role _role) external {
        require(_role != Role.None, "Invalid role");
        require(!users[msg.sender].isRegistered, "Already registered");
        
        users[msg.sender] = User(msg.sender, _role, 50, true);
        allUsers.push(msg.sender);
    }

    // Helper function for external contracts to check registration
    function isUserRegistered(address _user) external view returns (bool) {
        return users[_user].isRegistered;
    }

    // Returns reputation for the matching engine
    function getReputation(address _user) external view returns (uint256) {
        require(users[_user].isRegistered, "User not found");
        return users[_user].reputation;
    }

    function updateReputation(address _user, int256 _change) external {
        require(users[_user].isRegistered, "User not found");
        
        uint256 currentRep = users[_user].reputation;
        if (_change > 0) {
            uint256 newRep = currentRep + uint256(_change);
            users[_user].reputation = (newRep > 100) ? 100 : newRep;
        } else {
            uint256 loss = uint256(-_change);
            users[_user].reputation = (currentRep <= loss) ? 0 : currentRep - loss;
        }
    }
}