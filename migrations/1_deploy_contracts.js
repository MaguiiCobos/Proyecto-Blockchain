const contratoVotacion = artifacts.require("Votacion")

module.exports = function(deployer) {
    deployer.deploy(contratoVotacion);
};
