//Use this configuration file to set up Truffle for your project.
// This file is used to configure the Truffle framework for Ethereum development.
module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,
      network_id: "*" // Match any network id
    }
  },
  compilers: {
    solc: {
      version: "0.8.13"
    }
  }
};

