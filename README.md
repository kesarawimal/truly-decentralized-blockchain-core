## A Truly Decentralized Consensus Protocol

#### This is the core implementation of a novel consensus protocol that accommodates true decentralization avoiding centralization of power.
---
### Research Contribution

With its recent surge in popularity, blockchain is now widely acknowledged as a potentially
disruptive technology (Pang, 2020). Most of the current popular permissionless blockchains are
meant to be decentralized but as they grow the system tent to be more centralized ruining the core
value of a blockchain.

The current pattern demonstrates that bitcoin's network is moving away from its pure,
decentralized protocol toward centralization and that any kind of centralization should be carefully
assessed in the context of the 51% attack (Beikverdi and Song, 2015). The contribution of this
study is important as the market seeks a truly decentralized protocol that avoids leading to the
centralization of power. The developed novel consensus protocol will accommodate true decentralization 
securing the core value of a blockchain.


>Beikverdi, A., Song, J., 2015. Trend of centralization in Bitcoin’s distributed network, in: 2015
  IEEE/ACIS 16th International Conference on Software Engineering, Artificial Intelligence,
  Networking and Parallel/Distributed Computing (SNPD). Presented at the 2015 IEEE/ACIS
  16th International Conference on Software Engineering, Artificial Intelligence, Networking
  and Parallel/Distributed Computing (SNPD), pp. 1–6.
  https://doi.org/10.1109/SNPD.2015.7176229
  
>Pang, Y., 2020. A New Consensus Protocol for Blockchain Interoperability Architecture. IEEE
  Access 8, 153719–153730. https://doi.org/10.1109/ACCESS.2020.3017549

### Requirements

#### Python version
Python 3.8

### Installation
Install packages with pip:
`pip install -r requirements.txt`

### Set Environment Variables
`export PYTHONPATH=.;`<br>
`export FLASK_APP=src/node/main.py;`<br>
`export FLASk_ENV=development`<br>

### Start Server
`flask run`<br>
Or run this command<br>
`python -m flask run`
