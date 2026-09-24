#!/usr/bin/env python3
"""Check the experiment-specific failure modes before interpreting outputs."""
from __future__ import annotations
import csv, glob, json, pathlib, re
from rdkit import Chem

ROOT=pathlib.Path(__file__).resolve().parents[1]
props={r['id']:r for r in csv.DictReader((ROOT/'tables/ligand_properties.csv').open())}
charge_rows=[]
for path in sorted((ROOT/'derived/pdbqt').glob('*.pdbqt')):
    atoms=[]
    for line in path.read_text().splitlines():
        if line.startswith(('ATOM','HETATM')):
            fields=line.split(); atoms.append(float(fields[-2]))
    expected=int(props[path.stem]['formal_charge'])
    charge_rows.append({'id':path.stem,'expected_formal_charge':expected,'pdbqt_gasteiger_charge_sum':round(sum(atoms),4),'pdbqt_atoms_including_polar_H':len(atoms),'within_rounding_0.01':abs(sum(atoms)-expected)<0.01})
with (ROOT/'tables/pdbqt_charge_check.csv').open('w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(charge_rows[0])); w.writeheader(); w.writerows(charge_rows)

runs=[]
for path in sorted((ROOT/'poses/native_0EU').glob('seed-*.pdbqt')):
    seed=int(re.search(r'seed-(\d+)',path.name).group(1)); text=path.read_text()
    sdf=ROOT/f'poses/native_0EU/seed-{seed}.sdf'
    mols=[m for m in Chem.SDMolSupplier(str(sdf),removeHs=False) if m]
    log=(ROOT/f'logs/docking/native_0EU/seed-{seed}.log').read_text()
    runs.append({'seed':seed,'pdbqt_models':text.count('MODEL '),'sdf_molecules':len(mols),'vina_completion_marker':bool(re.search(r'^\s*20\s+-',log,re.MULTILINE)),'has_vina_error':'ERROR' in log.upper()})

inspection=json.loads((ROOT/'derived/structure_inspection.json').read_text())
redocking=json.loads((ROOT/'derived/native_redocking_summary.json').read_text())
summary={
 'identity_check': inspection['current_identity']['uniprot_accession']=='O00763' and inspection['current_identity']['organism']=='Homo sapiens',
 'assembly_check': inspection['site']['symmetry_mate_contacts_within_4.5_A']>0 and inspection['assemblies']['2']['oligomeric_details']=='dimeric',
 'native_ligand_check': inspection['native_ligand']['heavy_atom_count']==36 and inspection['native_ligand']['heavy_atom_occupancy_min_max']==[1.0,1.0],
 'charge_checks_all_within_rounding': all(x['within_rounding_0.01'] for x in charge_rows),
 'stereochemistry_and_charge_notes': '0EU S retained before/after conformer generation; neutral PRL has no stereocenter; protonated PRL retains +1 and has unspecified tetrahedral ammonium stereochemistry. The input does not assert one stable nitrogen stereoisomer; no inversion or proton-exchange kinetics were modeled or inferred.',
 'coordinate_mapping_check': redocking['method']['atom_mapping_check'] + '; RMSD analysis then requires stereochemistry-preserving graph matches and uses no coordinate alignment.',
 'run_output_checks': runs,
 'failed_output_check': all(x['pdbqt_models']==20 and x['sdf_molecules']==20 and x['vina_completion_marker'] and not x['has_vina_error'] for x in runs),
}
(ROOT/'derived/validation.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
if not all([summary['identity_check'],summary['assembly_check'],summary['native_ligand_check'],summary['charge_checks_all_within_rounding'],summary['failed_output_check']]):
    raise SystemExit('validation failed')
