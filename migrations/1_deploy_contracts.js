const bloque = artifacts.require("smartContract")

module.exports = function(deployer) {
    deployer.deploy(bloque);
}

