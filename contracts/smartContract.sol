// SPDX-License-Identifier: UNLICENSED
//truffle.cmd compile

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

    struct Resultados {
        uint votoBlanco;
        uint contadorPresidente1;
        uint contadorPresidente2;
        uint contadorPresidente3;
        uint contadorGobernador1;
        uint contadorGobernador2;
        uint contadorGobernador3;
        uint contadorIntendente1;
        uint contadorIntendente2;
        uint contadorIntendente3;
        uint contador;
    }

    function votosPorCandidato() public view returns (Resultados memory) {
        uint votoBlanco = 0;
        uint contadorPresidente1 = 0;
        uint contadorPresidente2 = 0;
        uint contadorPresidente3 = 0;
        uint contadorGobernador1 = 0;
        uint contadorGobernador2 = 0;
        uint contadorGobernador3 = 0;
        uint contadorIntendente1 = 0;
        uint contadorIntendente2 = 0;
        uint contadorIntendente3 = 0;
        uint contador = 0;
        for (uint i = 0; i < votos.length; i++) {
            if( votos[i].presidente == 0 && votos[i].gobernador == 0 && votos[i].intendente == 0) {
                votoBlanco++;
            } else {
                if (votos[i].presidente == 1) contadorPresidente1++;
                else if (votos[i].presidente == 2) contadorPresidente2++;
                else if (votos[i].presidente == 3) contadorPresidente3++;
                
                if (votos[i].gobernador == 1) contadorGobernador1++;
                else if (votos[i].gobernador == 2) contadorGobernador2++;
                else if (votos[i].gobernador == 3) contadorGobernador3++;
                
                if (votos[i].intendente == 1) contadorIntendente1++;
                else if (votos[i].intendente == 2) contadorIntendente2++;
                else if (votos[i].intendente == 3) contadorIntendente3++;
            }
            contador++;
        }

        return Resultados(
            votoBlanco,
            contadorPresidente1,
            contadorPresidente2,
            contadorPresidente3,
            contadorGobernador1,
            contadorGobernador2,
            contadorGobernador3,
            contadorIntendente1,
            contadorIntendente2,
            contadorIntendente3,
            contador
        );
    }

}
