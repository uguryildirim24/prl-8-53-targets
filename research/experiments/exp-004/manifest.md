# exp-004 manifest

> **Public release note.** Some files in this repository were edited before publication: local absolute paths were made repo-relative, a machine hostname was removed, and material that is not redistributed here was taken out. Every SHA-256 recorded in this folder, including `SHA256SUMS`, was recomputed against the published files, so the hashes verify what is here rather than the internal working copy. No result, pose, score, table or log value was changed.


Generated inventory of experiment files. Reused exp-003 and retained identity/source bytes are not duplicated; `inputs/source_manifest.json` and `inputs/presearch_inventory.json` pin them by hash. `manifest.md` excludes itself; `SHA256SUMS` includes it.

| File | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `commands.md` | 3435 | `1733eb0aa16c42530e1ac47e85367ee2c7ac9c1693a5a3d1845667f6e1656ca1` | protocol/report/provenance |
| `derived/identity_graph_and_conformers.json` | 15534 | `399414a5602cabd8877fecdf964c9be2cd8ddd08e453c3f1c7e0130dc0591f16` | prepared input/generated analysis |
| `derived/pdbqt/prl_neutral_c1.pdbqt` | 2283 | `6929e857d443ecb9ce10bc3d8cc141fb15c18675c2443d01c90c8be28d166e4d` | prepared input/generated analysis |
| `derived/pdbqt/prl_neutral_c2.pdbqt` | 2283 | `5d2deaba66143e6a5e2d4117903556d507cc43056056bd56cf9bd74836eabf96` | prepared input/generated analysis |
| `derived/pdbqt/prl_protonated_c1.pdbqt` | 2381 | `607fdae0907e772dd826b29c05875a0f68d726c9b8eaac001d6b6aa1db3e8773` | prepared input/generated analysis |
| `derived/pdbqt/prl_protonated_c2.pdbqt` | 2380 | `47e88f79cc94e8489c2316e4f18cb887a7f1cfc9e211fb992769db0e9321d49f` | prepared input/generated analysis |
| `derived/presearch_validation.json` | 4220 | `9cb1052bcd621bd769f99e3b8f19b50d4cc36270d20c179a273709338243188b` | prepared input/generated analysis |
| `derived/prl_neutral_c1.sdf` | 3835 | `c25f93de3cb8bb14e289bf75829f942f2b420e004db86e0d8f6a6a763e4a1ef7` | prepared input/generated analysis |
| `derived/prl_neutral_c2.sdf` | 3835 | `808a48393792d2afeb1f7bf0ab51dcd317fc074dcb37f690987840ad92b5124c` | prepared input/generated analysis |
| `derived/prl_protonated_c1.sdf` | 3942 | `82735a89fdb9763d4abb15fd860c73c1a20afd54846c00bda7653c1e3af16620` | prepared input/generated analysis |
| `derived/prl_protonated_c2.sdf` | 3942 | `d94ca5cadda9f99a75fa83ca36905519c16873c67692629840c9cba1e673020f` | prepared input/generated analysis |
| `derived/results_summary.json` | 7794 | `1b71d097e3ac9a3eff75b50f546e902b53f3d4fc2ab6d67e77fd6ba8b5b24026` | prepared input/generated analysis |
| `derived/validation.json` | 7525 | `54c345dfe7b0b15969bdd512f9fbbeb5fc70605792e9d62577c1a59d9a90c203` | prepared input/generated analysis |
| `environment.txt` | 1127 | `eef46d7f13835f44fee40affbf8ccd3a7185ce7991949e0135c3723684c011a3` | protocol/report/provenance |
| `inputs/presearch_inventory.json` | 3379 | `7ebd98dfd2c38c6546ebcbdd59aab6d808ad102aba9698726520f98a6eac9ae7` | source/pre-search ledger |
| `inputs/source_manifest.json` | 2745 | `ab339c1fa8dd626d91652353e6e1fd5819de529c5599ab86b638e15d341de6d8` | source/pre-search ledger |
| `logs/analyze_results.stderr.txt` | 755 | `d44ec34f00ec812a022109fffcd646b54a82c5b6641c711725452d22de56b692` | raw command/resource log |
| `logs/analyze_results.stdout.txt` | 1331 | `1b0c3f665510c3c63437bf53fb539c949695f68e31434ad0956d6fd215b19f10` | raw command/resource log |
| `logs/build_manifest.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/build_manifest.stdout.txt` | 38 | `6770d0bd6039d6bae8d2efae6c84b97a87cdafd968a6916ade63594cb29134db` | raw command/resource log |
| `logs/build_presearch_inventory.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/build_presearch_inventory.stdout.txt` | 47 | `37dc051331e6a9d5b2dbeebe5f00cb1dd6c07dbc3e2c3477a9b88ba82c78228d` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5301-export.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5301-export.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5301.monitor.json` | 13138 | `366dd5c9174578644fec7a59ea392468b0caa2ba26484e596817bafa7966e200` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5301.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5301.stdout.txt` | 2718 | `f3434fea6def82f8834858950f8f2cccc9cd3e042a1d56eb1200f1046cc7ce0f` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5302-export.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5302-export.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5302.monitor.json` | 13139 | `767917327a37de19df629c5bbf1ee50b5bbaee0e258a54ee13c2dcb1a9507ded` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5302.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5302.stdout.txt` | 2718 | `4fb0d69c77a3c80fed07fb4cb7541fffaf0c76fd45cd828609b11318c3ffc1c2` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5303-export.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5303-export.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5303.monitor.json` | 13136 | `53d59d6f6cd7c592d42653474d423caf91841b6b8906d3f74ec26fae8244e2a7` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5303.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c1/seed-5303.stdout.txt` | 2718 | `c42317da393d6d837507d2a2ea70884276d146331382a27f8d11cde1bf041008` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5301-export.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5301-export.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5301.monitor.json` | 13137 | `89cc4d1e63af35a660f41f7c94de45e80ec28fe55d876dc3a6b0e1fd01823008` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5301.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5301.stdout.txt` | 2718 | `7cad4cc8f9e4b00bafe169567adb4f197c9ffd0dab51c9b5cd38409710eb5cf1` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5302-export.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5302-export.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5302.monitor.json` | 13138 | `3f230ec58c2182145a26f3c83d09ba951445eada54ba15366d14b29139c74bbf` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5302.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5302.stdout.txt` | 2718 | `1ab49edbdd77a9b442bf716793f290938cb2f79d0af3f2a3b59b7bfdc038ad09` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5303-export.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5303-export.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5303.monitor.json` | 13139 | `29df8f487501ed1773d9689ddd47f9d112e042bddd1928ff9229311fbb277da1` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5303.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_neutral_c2/seed-5303.stdout.txt` | 2718 | `e8d0bd64faa81f4a1e77afec93008423952340784a6b832d8fd6e42a3e47d061` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5301-export.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5301-export.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5301.monitor.json` | 13156 | `a6287599f110858bc2ec28b4176039838184136d0adbcccbc8e52a9a3d629f7c` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5301.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5301.stdout.txt` | 2721 | `cbb80206173e89e89818440c07d7cc72993606af34bf1a3a416bf4b4024b52d8` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5302-export.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5302-export.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5302.monitor.json` | 13158 | `be28e5f2ae7ef5b83ec1955b7485432c3b148b13ca1ccc595c6d9287610e15bd` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5302.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5302.stdout.txt` | 2721 | `6c68c8ac17e43fb3f104bc247f2424f9ff02ef578ecabd23128a88f5969c550e` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5303-export.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5303-export.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5303.monitor.json` | 13160 | `bd5d2fd3569234ccaa21358b85645967e031f5cd1785ae71c26d206cb599e4c9` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5303.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c1/seed-5303.stdout.txt` | 2721 | `a1999223631b15deb53f5707e54c4b04ed8964d737496a05b52e61a147854675` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5301-export.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5301-export.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5301.monitor.json` | 12781 | `2537d1c8c2b3243f3c94169f582fdd501d0a064320467d3c1e43e426f500e526` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5301.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5301.stdout.txt` | 2721 | `9b2958ff83eb0a766e921986bf8ce21f4bd4d0a143c4f133a1d84cb8a06f0c18` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5302-export.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5302-export.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5302.monitor.json` | 13061 | `d78ffde23ea3d72f75cc9f8ef56230bfcfdec91c775fb75608ad2dbb86eead1f` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5302.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5302.stdout.txt` | 2721 | `ede926849890f6b055607dbb72d29181d610072bf92225ce1c30ba930b7ebc31` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5303-export.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5303-export.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5303.monitor.json` | 13157 | `b81c39bae2666c3589667a20fc75728af8f5aae028c127f84f3196ea4483a727` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5303.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/docking/prl_protonated_c2/seed-5303.stdout.txt` | 2721 | `1398f3c76e1d0a773defe87b122de2c9ef796f713b0b4defc806aa23ba4feabd` | raw command/resource log |
| `logs/ligand-preparation/prl_neutral_c1.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/ligand-preparation/prl_neutral_c1.stdout.txt` | 135 | `8f13b69c763278d183de36bb0149cb01e2557ff091944fa32edea3812f1eda92` | raw command/resource log |
| `logs/ligand-preparation/prl_neutral_c2.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/ligand-preparation/prl_neutral_c2.stdout.txt` | 135 | `8f13b69c763278d183de36bb0149cb01e2557ff091944fa32edea3812f1eda92` | raw command/resource log |
| `logs/ligand-preparation/prl_protonated_c1.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/ligand-preparation/prl_protonated_c1.stdout.txt` | 135 | `8f13b69c763278d183de36bb0149cb01e2557ff091944fa32edea3812f1eda92` | raw command/resource log |
| `logs/ligand-preparation/prl_protonated_c2.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/ligand-preparation/prl_protonated_c2.stdout.txt` | 135 | `8f13b69c763278d183de36bb0149cb01e2557ff091944fa32edea3812f1eda92` | raw command/resource log |
| `logs/prepare_inputs.stderr.txt` | 753 | `f720d3ba4151464ff59560774edb24d3a515b9d325847e0c1a50c03431749096` | raw command/resource log |
| `logs/prepare_inputs.stdout.txt` | 571 | `5200b2141c60052b45abd358fb91c317ea02810ebf2c5e0d1780b39c6b7bb87f` | raw command/resource log |
| `logs/prepare_ligands.stderr.txt` | 753 | `cbfdf692c80a7184f9409921b6fa3886ceafdd08046ac3d3054fa67610a9621b` | raw command/resource log |
| `logs/prepare_ligands.stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | raw command/resource log |
| `logs/run_all_searches.stderr.txt` | 755 | `720535e2d657965df67eef96c7ae0821e456fe0b2d124755ed9b0d36e485f5a0` | raw command/resource log |
| `logs/run_all_searches.stdout.txt` | 2416 | `a930381a5bd15e4a080e19fe6975f9343a1605633a2de8f956c5046f2a507b48` | raw command/resource log |
| `logs/validate_outputs.stderr.txt` | 753 | `c72d392bb8e567e98d520e2cd9ad2b8ecfadef18afe4a0ad97d4a14f1474bada` | raw command/resource log |
| `logs/validate_outputs.stdout.txt` | 146 | `033ad9ef3835b24ae49a487703099f75f01d39ce0be2bfb46b473971709fa89f` | raw command/resource log |
| `logs/validate_presearch.stderr.txt` | 753 | `e08cca85c9acd395841dd40cbf3661b46e95c07c21c56f8f4c1b3bfc83947b1b` | raw command/resource log |
| `logs/validate_presearch.stdout.txt` | 108 | `053ac1f5d14e20c7e6b1770cd5c961f69d373d9e7f6e0d3ada0474cf90e5fb7c` | raw command/resource log |
| `poses/prl_neutral_c1/seed-5301.pdbqt` | 50051 | `45ba9ab4e01fe6c36bea7e781d5939e0a47c88bdcb24712beddf0c93a1fca6df` | raw search output/export |
| `poses/prl_neutral_c1/seed-5301.sdf` | 74264 | `e0b682a863d6622d9b52220fbad4d4ff369e4b52b3bf88696f2394a9aecfb8d6` | raw search output/export |
| `poses/prl_neutral_c1/seed-5302.pdbqt` | 50051 | `ccfba58a8c837cefcc5165fa68aa90a3b96d7905167968f97755f1dd56e87753` | raw search output/export |
| `poses/prl_neutral_c1/seed-5302.sdf` | 74260 | `9bf8642d263b984dae837eda1272b4f0605c14561404793772cd636eb40ada06` | raw search output/export |
| `poses/prl_neutral_c1/seed-5303.pdbqt` | 50051 | `7e5d9574039ee1a1b0d30a803d43e5922ae9be9aa3df299eed9a514ee48e0782` | raw search output/export |
| `poses/prl_neutral_c1/seed-5303.sdf` | 74261 | `6bb620f09505ebf93c456ea8a9bbe433687be9a23e361279eefc9f7925aeead7` | raw search output/export |
| `poses/prl_neutral_c2/seed-5301.pdbqt` | 50051 | `e22914fea4349b0c5a483353c324dab16fcb6616410aa509a94b8822523d23f8` | raw search output/export |
| `poses/prl_neutral_c2/seed-5301.sdf` | 74263 | `4de8ce85d0ad7c97809bc6360c4050647f5c8f94e5a1c02c0e6e78b1d2c808c6` | raw search output/export |
| `poses/prl_neutral_c2/seed-5302.pdbqt` | 50051 | `efcbb47f2864db96d0516b36fa8aaadbe9c670348af9a243986136a96de26404` | raw search output/export |
| `poses/prl_neutral_c2/seed-5302.sdf` | 74260 | `abfe773355f8213c659d71c76ae4b3961cd27b95586012a80c29768d4406115b` | raw search output/export |
| `poses/prl_neutral_c2/seed-5303.pdbqt` | 50051 | `0c2539194cf8b8c1c0754b0eb1171fca342fc132825a24b03bcab8dad91ccda6` | raw search output/export |
| `poses/prl_neutral_c2/seed-5303.sdf` | 74264 | `145ecd017104678cb497f60508d3fc5b7eef82a7fa6af8afc4bf810b5526251c` | raw search output/export |
| `poses/prl_protonated_c1/seed-5301.pdbqt` | 52011 | `81472d675505004d07d8e01cfea74cb6b0f282ed9ddbed5d18af994122d20422` | raw search output/export |
| `poses/prl_protonated_c1/seed-5301.sdf` | 76284 | `3c1f153e2cf8177baadc1bbe284f970255d5a267f5480aeeedbfda9d41780f41` | raw search output/export |
| `poses/prl_protonated_c1/seed-5302.pdbqt` | 52011 | `8db8293422ef748a46f69586184705150fa5505df72574af3b8d2487c2051753` | raw search output/export |
| `poses/prl_protonated_c1/seed-5302.sdf` | 76280 | `f493e9f8e51f490dad728b7ab5dcc1a611a07c11096bb124b4f98455f1c6f352` | raw search output/export |
| `poses/prl_protonated_c1/seed-5303.pdbqt` | 52011 | `49e7476a383b86505e0d6ed32b658657c748c8dbce6c3f4e33ba3496bdbe6d00` | raw search output/export |
| `poses/prl_protonated_c1/seed-5303.sdf` | 76280 | `7ca920ebb58429a566005f9a2f382d4e2303f6e3b19e2af61db4c495ea19b04f` | raw search output/export |
| `poses/prl_protonated_c2/seed-5301.pdbqt` | 51991 | `899b19398718c5abadda849c7289e9b53aee08c7d93f4dd83994e3e00168b995` | raw search output/export |
| `poses/prl_protonated_c2/seed-5301.sdf` | 76282 | `c0c531a5a44714f8cc0f8d43e78073a8d69b55b629a4517529df8ae8ca781630` | raw search output/export |
| `poses/prl_protonated_c2/seed-5302.pdbqt` | 51991 | `3e7e7a58ff08c955a6edb50f07e21b445d454a58c4274487ca710cdf1d38f504` | raw search output/export |
| `poses/prl_protonated_c2/seed-5302.sdf` | 76282 | `9059af418e8f5ec3a0a868afbe989cddf8f3945c54b203f1cce80948bc501420` | raw search output/export |
| `poses/prl_protonated_c2/seed-5303.pdbqt` | 51991 | `79af78ed200a00df40ffb849b98bb38a6725bb8775e2e8f7b7006c0178b6f9ce` | raw search output/export |
| `poses/prl_protonated_c2/seed-5303.sdf` | 76284 | `be24df94e8224c819bd2a2a6497f148d2fa9618e7fce36c7703de2d7cf78aafe` | raw search output/export |
| `protocol-prerun.md` | 8351 | `e91dffe6312cf55d2d2dfdce696b5053905eb9980620b1c187f9823cf95740e8` | protocol/report/provenance |
| `results.md` | 11467 | `6446eb2f1d023e0bb58835f4feff7b9fa2a7d43170ab21498f7679174378d0d7` | protocol/report/provenance |
| `scripts/analyze_results.py` | 12043 | `0e972deaeae4e2a050bca174d297f2ac5429e58f92633abbc43b4b031b015adf` | reproduction script |
| `scripts/build_manifest.py` | 1794 | `c89a0a3562d36f24488a297a5fdcef7d4e0477cb921f8f7dbfa1548215a1e268` | reproduction script |
| `scripts/build_presearch_inventory.py` | 1726 | `eb53c4217c96bcb27b434c4cb99e58f74a5b8010c6f0d87e71ab659e1bae5f47` | reproduction script |
| `scripts/prepare_inputs.py` | 13069 | `64ab0d58e6aed7966aef0883d06d4dde62ef1e779be6b9cb42cbf87b260c4f6f` | reproduction script |
| `scripts/prepare_ligands.sh` | 733 | `43ab6a6010fb021b331c5f62fbfd012cfbb85c6f2f8f223225140eca01c5a81e` | reproduction script |
| `scripts/run_all_searches.sh` | 1029 | `8b64223f5a7f2a48f592b810f3891d3d8fa07b4ba6f221a012625401a42a5468` | reproduction script |
| `scripts/run_vina_one.py` | 6518 | `1489f5706767213bf9f9008708a24bef709194e368af327e7031e08caebb1c89` | reproduction script |
| `scripts/validate_outputs.py` | 7265 | `3dc22df99c0c9f5f27298eec2e238e7314cf1176a74e983a2e9e68a34ebd5af7` | reproduction script |
| `scripts/validate_presearch.py` | 6022 | `5a257f74210f9ea931bb50d3149fd4b76898de21c889de3b7d1a759c3950fc07` | reproduction script |
| `tables/all_poses.csv` | 74515 | `e6d8065e185db84e946d65d745384f1b4cad2c32646738f25b0c7eea971b4ade` | generated analysis table |
| `tables/pose_pairs.csv` | 1342615 | `7cf8deeca2c4fd3f8df4bbfc069c6358eef465550f0f33f2c7bebccf2005abdb` | generated analysis table |
| `tables/presearch_ligand_checks.csv` | 639 | `e6c206180ecd2bdf5b8227d275996453fe6f04c38ac37609fe855f03174f48d0` | generated analysis table |
| `tables/runs.csv` | 2078 | `f12f07c0796e0d696920cce5ee529a4927a8f4b38e08edf24872510e5ff0a9ca` | generated analysis table |
