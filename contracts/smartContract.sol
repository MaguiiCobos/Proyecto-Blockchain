// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.13;

contract Votacion{

    struct Voto{
        uint presidente;
        uint gobernador;
        uint intendente;
    }

    Voto[] public votos;

    function guardarVoto(uint _presidente, uint _gobernador, uint _intendente) public {
        votos.push(Voto(_presidente, _gobernador, _intendente));
    }

    function obtenerVoto(uint index) public view returns (uint, uint, uint) {
        Voto memory v = votos[index];
        return (v.presidente, v.gobernador, v.intendente);
    }

    function totalVotos() public view returns (uint) {
        return votos.length;
    }

    
    
    




}
