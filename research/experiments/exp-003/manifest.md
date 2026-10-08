# exp-003 manifest

> **Public release note.** Local absolute paths and a machine hostname were removed before publication. Unavailable service material was not redistributed. This file inventory and `SHA256SUMS` describe published bytes after documentation edits and removal of empty or duplicate log captures. Source inventories and historical analysis reports remain unchanged. See `docs/release-review.md` from the repository root for replay limits.

Generated inventory of experiment files. Preserved official source bytes remain in `../../alternative-coordinate-evidence/raw/`; `inputs/source_manifest.json` records and verifies their hashes without duplicating them here. `manifest.md` excludes itself; `SHA256SUMS` covers it.

| File | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `commands.md` | 4301 | `e7f99c0fb7029e2433e6e1e8cc7fd18dc605a61ede893750f45dd2f4d5ebb7b2` | protocol/report/provenance |
| `derived/ligand_graph_and_conformers.json` | 4376 | `fa247811271a5c2b28badd5807005803f6e096e024ff61e9f406f768b422fa25` | prepared input/generated analysis |
| `derived/native_8PR_bound_reference.pdb` | 1900 | `ae3d1ed7627872a7bd66e1e7bbd9632ff05b875b8fda15e255be2aa2ea30c478` | prepared input/generated analysis |
| `derived/native_reference.json` | 4537 | `c7b58a8f5337d64869a1e692ce040683e1ca224031891a5d7a560a9dbab0ef1f` | prepared input/generated analysis |
| `derived/paroxetine_neutral.sdf` | 4009 | `baf11af5123115cba0f57f0f9a7fef796876ad266195ce7e80d0e215c7acf176` | prepared input/generated analysis |
| `derived/paroxetine_protonated.sdf` | 4113 | `dffa7fa2ab91f942b366348c30c61ec1ea37a69ee885a450080b28225eb7eec9` | prepared input/generated analysis |
| `derived/pdbqt/paroxetine_neutral.pdbqt` | 2599 | `168bc4b5ccbd25f631ac807521e3efa0f54731d0af5ae06d974f9b787b43b981` | prepared input/generated analysis |
| `derived/pdbqt/paroxetine_protonated.pdbqt` | 2695 | `47fc58d71198a8084eb01e1b5c7d75fb4a85857087cb7e97889df0bc5a037f47` | prepared input/generated analysis |
| `derived/preparation_audit.json` | 2135 | `09797b3762de4d23a717bfc40fd510bb2016df1bfa597c18db7728eaa42db419` | prepared input/generated analysis |
| `derived/receptor_6vrh_chainA_resolved_protein.pdb` | 340600 | `52a7788f5b518b14fb822002e2ca61d7d9b8b60849a55a2cbb1734fcf0524dde` | prepared input/generated analysis |
| `derived/receptor_6vrh_primary.box.pdb` | 915 | `aa797f4e5c789561ae6b56a0c55e853ffdfa77555eeb578c4e1dc5c03281c1c2` | prepared input/generated analysis |
| `derived/receptor_6vrh_primary.pdbqt` | 411920 | `01ec06e6bfb7708c389bcfc884c929547114b4a9318f8a1f6861c43ab793a5cc` | prepared input/generated analysis |
| `derived/receptor_6vrh_primary_prepared.pdb` | 687840 | `de88b8085a444a92a9453d5b57908361c4c858db2834cdce3c7a564d366bf866` | prepared input/generated analysis |
| `derived/results_summary.json` | 3896 | `f206f28683f32ae8b5784816f8f2b10133519fd842300ff3a8d688078dba14c8` | prepared input/generated analysis |
| `derived/validation.json` | 4659 | `abc7a20eabe3e10b082541cce602653f153158753b53578df8d972b2d3171e4c` | prepared input/generated analysis |
| `derived/vina_box.txt` | 104 | `51039da260ded8df703a54880e09dd2707174408fc6ce29cbaffe6a9e01a53c7` | prepared input/generated analysis |
| `environment.txt` | 1171 | `dd8e58f370e8012d050f6107eae059dbc72a7f384d4250d81eef852a8dccd999` | protocol/report/provenance |
| `inputs/source_manifest.json` | 1529 | `e2e938669d741bfa95d7facd170723b632d51850346b2602098e17f22f714b1f` | source ledger |
| `logs/analyze_results.stderr.txt` | 753 | `911f73b1b1fb21798f8c01cb2d5b91a30053080c8466ca2db8be36de62fd0318` | raw command/resource log |
| `logs/analyze_results.stdout.txt` | 36 | `957968bdb34d43170392b86fa81d6f48cfbe94952aeebcfa338d824744d10bc4` | raw command/resource log |
| `logs/build_manifest.stdout.txt` | 36 | `a291bb05676448b0d3ea61fd788d3ac9ac79dc775e0cb89905c17548de6c62ae` | raw command/resource log |
| `logs/checksums.stderr.txt` | 51 | `7dcfceb713d22c43bdfb4d3dac5789bbc5e360e60e041dfd2bc33c15b8007be7` | raw command/resource log |
| `logs/checksums.stdout.txt` | 4276 | `07c5ea11f2601390f172ab031bf548a4a91a5725d4bc8d07497a4848e5f1b544` | raw command/resource log |
| `logs/docking/paroxetine_neutral/seed-2301.monitor.json` | 10674 | `71bb8ad83c6e777773bed8526b4754138b604940a03f2389f574d455e600893e` | raw command/resource log |
| `logs/docking/paroxetine_neutral/seed-2301.stdout.txt` | 2636 | `ccd82cfab9d7007b68db763733e8048ed784ba66127331e9ac3c5aca13e7960b` | raw command/resource log |
| `logs/docking/paroxetine_neutral/seed-2302.monitor.json` | 10677 | `966e7bc7fe6fb687215864588a6de32a18c7219dc16b94b5df4c1150198aa020` | raw command/resource log |
| `logs/docking/paroxetine_neutral/seed-2302.stdout.txt` | 2636 | `e716bbd9abbca000681d1aaa7a8f7403977e0e5eda7514acfbdba42b2f22fce5` | raw command/resource log |
| `logs/docking/paroxetine_neutral/seed-2303.monitor.json` | 10677 | `69ba6cbf10e4ccd7e3bfcd909aba2bd70ada4f78f0aa35a8d83958993f81b8d3` | raw command/resource log |
| `logs/docking/paroxetine_neutral/seed-2303.stdout.txt` | 2636 | `1dab25b993c36d27b4f10872c7c4d7b7749938124b28f8babcfdeb26936cbc5a` | raw command/resource log |
| `logs/docking/paroxetine_protonated/seed-2401.monitor.json` | 10973 | `c55320108b2374e6f776160c9e8dca42236ea3a5bd026969d5eb4a058527ddc7` | raw command/resource log |
| `logs/docking/paroxetine_protonated/seed-2401.stdout.txt` | 2639 | `13bc2443cd7a99ce09c482e786268be6107bb2199538eec23c3c25ab9092bdb7` | raw command/resource log |
| `logs/docking/paroxetine_protonated/seed-2402.monitor.json` | 11029 | `fbc6e6d9d959c642c9f568616ac9f768444352e052f5becc45faa3feafb1843e` | raw command/resource log |
| `logs/docking/paroxetine_protonated/seed-2402.stdout.txt` | 2639 | `8995ba470b8c12e7ba6ee469d9fcf33e596dc007f72c14d4c19bc112b0fe68e9` | raw command/resource log |
| `logs/docking/paroxetine_protonated/seed-2403.monitor.json` | 10979 | `e52e9bf7a08d9c71120f043f0d9b4f340913269c6a6e748e2835dca035235b01` | raw command/resource log |
| `logs/docking/paroxetine_protonated/seed-2403.stdout.txt` | 2639 | `81aed39d35375b7b3dfb7c2acc6b25e25360c685fc3778624763f5f48c362323` | raw command/resource log |
| `logs/ligand-preparation/paroxetine_neutral.stdout.txt` | 135 | `8f13b69c763278d183de36bb0149cb01e2557ff091944fa32edea3812f1eda92` | raw command/resource log |
| `logs/ligand-preparation/paroxetine_protonated.stdout.txt` | 135 | `8f13b69c763278d183de36bb0149cb01e2557ff091944fa32edea3812f1eda92` | raw command/resource log |
| `logs/prepare_docking_inputs.final.stderr.txt` | 753 | `6a8f94396c121248b1dc3ea32e84aeb7b777efcd9cee2e05609f97ff46c260aa` | raw command/resource log |
| `logs/prepare_docking_inputs.final.stdout.txt` | 568 | `d16b430eb6fbe866e7f23214e54b2227e9a56f4eff7c5330e9e104cad1e3c5e4` | raw command/resource log |
| `logs/prepare_docking_inputs.stderr.txt` | 1891 | `d66a19ff829693ccbdf781a95c980fa43f67757744a62541f084ab962430e6bd` | raw command/resource log |
| `logs/prepare_docking_inputs.stdout.txt` | 719 | `538080baee92ef92d162a5d5b0bf9979e1a0ebc3eb0c25030b39970592f37684` | raw command/resource log |
| `logs/prepare_inputs.final.stderr.txt` | 753 | `88daec6446bebf27aba5a38ccc2558160b188d82cc15d9ef06c9a099604a2a47` | raw command/resource log |
| `logs/prepare_inputs.final.stdout.txt` | 206 | `527f434b13986971096edc0cfe1ff99dc0c846a2a1159464b471d78dbf12b8f8` | raw command/resource log |
| `logs/prepare_inputs.stderr.txt` | 753 | `b7e571edc99a6ee6d7d876e253fd722f90f2ff7d7cd702fa26c921ac9371b303` | raw command/resource log |
| `logs/run_all_searches.stderr.txt` | 755 | `cb9476eaa55412dc6aec7e27694a5999eb4ddb6cf858134837f870310bd5e638` | raw command/resource log |
| `logs/run_all_searches.stdout.txt` | 1227 | `84bd897475491085d931383c96951e7b4b41701ca23622dd2afd9143def2796c` | raw command/resource log |
| `logs/validate_outputs.stderr.txt` | 753 | `24d2413f5a4cbe860a4302987d50e63ffe5f291d50f33646ea1cc75e050a20ce` | raw command/resource log |
| `logs/validate_outputs.stdout.txt` | 51 | `6d1f7b181c5016cf15cf818c8874bf160fabadd295782afdeaf86cd983fb4429` | raw command/resource log |
| `poses/paroxetine_neutral/seed-2301.pdbqt` | 56371 | `7d7a1da5ad53df073a1476fe7a54c5864d3e8aafc9fda35e27f85eb24d34c3ce` | raw search output/export |
| `poses/paroxetine_neutral/seed-2301.sdf` | 78106 | `14bf044706bdb21178c3fab8b8d9b42336fc207817cb64e9d9906b44f6e39882` | raw search output/export |
| `poses/paroxetine_neutral/seed-2302.pdbqt` | 56371 | `e0b69e0248a511b4ff0e8192a9d90289c56a1f201ad1c676b6bcb489aa7538df` | raw search output/export |
| `poses/paroxetine_neutral/seed-2302.sdf` | 78108 | `7a46caa46734601954be87176c23419d427e30c86d1dd897e6209190d3fdbe78` | raw search output/export |
| `poses/paroxetine_neutral/seed-2303.pdbqt` | 56371 | `fe8080ce4a9d7d6b293f1a1d9df23ffd1dd7e1ff0796a7d6d33cc2e2752bac72` | raw search output/export |
| `poses/paroxetine_neutral/seed-2303.sdf` | 78105 | `a773a0d42861199f8f9bd2908e94a4bef75a1bf68d733300250cbd725e5be37e` | raw search output/export |
| `poses/paroxetine_protonated/seed-2401.pdbqt` | 58291 | `b8fa536ecce3e0ff0d5dcc99ac2c1a3ec6e09e86aa118003e9db242927211c60` | raw search output/export |
| `poses/paroxetine_protonated/seed-2401.sdf` | 80126 | `3f6303780e883008e36def81a199f8c77240f3dc7481ab37eecdaa09cdcded1b` | raw search output/export |
| `poses/paroxetine_protonated/seed-2402.pdbqt` | 58291 | `ed07f576eb43b7e2bac1c3aa632b14fbac04b3bef99d89595dafaf9313212576` | raw search output/export |
| `poses/paroxetine_protonated/seed-2402.sdf` | 80124 | `6a29b323ccdbdef47bb7cc65b459d1db969541d8035d97df22ad3e003607b7f0` | raw search output/export |
| `poses/paroxetine_protonated/seed-2403.pdbqt` | 58291 | `bd0b717ae540033375a1dc8e9f7a52eec308c8fe2f97cd51374d162074d33972` | raw search output/export |
| `poses/paroxetine_protonated/seed-2403.sdf` | 80123 | `50a2ef91ac421eb9e05ba76d1a3466337f27af3ae2dc3469def3c3a82d043ad5` | raw search output/export |
| `protocol-prerun.md` | 10296 | `ba6472c32d1a2af47fec62b459e61ccb223aed4cb384b43796ccefcae4830cd2` | protocol/report/provenance |
| `results.md` | 9851 | `97d5a2beec12e4397933922c26fe7d62fc1ac657d5ee5e8d0cc8dbebe52961b3` | protocol/report/provenance |
| `scripts/analyze_results.py` | 8574 | `82167ff374e18743c185888390043ad86b305658eabf7f53cac91d024d397e3d` | reproduction script |
| `scripts/build_manifest.py` | 2185 | `518ae1684d50d9840996cfb16734b621daf165d5d56c29741d9121c4403ca4c3` | reproduction script |
| `scripts/prepare_docking_inputs.sh` | 1346 | `b5a41d90c78bb3d14c0584492b11063a70a30238e75a6b8463858acdd91aeada` | reproduction script |
| `scripts/prepare_inputs.py` | 15364 | `5c967a4e028c56e149bf52f5b4edec596153b7c58dae9fc7d9f9b42323d10dd3` | reproduction script |
| `scripts/run_all_searches.sh` | 1096 | `e8e1b70aba396445b0d456d3334ab61138b88140162de68312d81a8194e5b19f` | reproduction script |
| `scripts/run_vina_one.py` | 6645 | `1eca00fd2cb74f3ce297b7079a378a3f6c7e9333e9727b7eadd74bddc2b298fb` | reproduction script |
| `scripts/validate_outputs.py` | 8062 | `df4ccc28083c49963f308dad908422db94cd095b8266eea260d23c6ecff1cf1d` | reproduction script |
| `tables/all_poses.csv` | 18048 | `d54f197279a6039bf09315e3c051799eb85dca01441da08cec679525166dd32b` | generated analysis table |
| `tables/ligand_charge_check.csv` | 183 | `135641bcd39497b8fcdb997df3824d7f141135df28a85c1057ca64bfbecf25c0` | generated analysis table |
| `tables/runs.csv` | 826 | `d36baf225fb3006a9d80afb6044e5b331eff543e63d31310eb4b7a3daaaf0d14` | generated analysis table |
