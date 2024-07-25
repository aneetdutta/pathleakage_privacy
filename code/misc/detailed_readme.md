Below is the overall structure of the code with the configuration ```project.yml```.

```bash
├── csv
│   ├── baseline_ble_project.csv
│   ├── baseline_lte_project.csv
│   ├── baseline_smart_ble_project.csv
│   ├── baseline_smart_lte_project.csv
│   ├── baseline_smart_wifi_project.csv
│   ├── baseline_wifi_project.csv
│   ├── multi_protocol_project.csv
├── data
│   ├── correctness_project.json
│   ├── full_coverage_ble_sniffer_location.json
│   ├── full_coverage_wifi_sniffer_location.json
│   ├── partial_coverage_sniffer_location.json
│   ├── raw_user_data_project.csv
│   ├── sniffed_data_project.csv
│   ├── user_data_project.csv
│   ├── user_mobility_project.json
├── design
│   ├── design_arch.pdf
│   └── design_arch.png
├── group
│   ├── aggregate_sniffer_timesteps.py
│   ├── aggregation.py
│   ├── grouping_algorithm_seq.py
│   ├── grouping_algorithm_tri_seq.py
│   ├── grouping_smart_algorithm_seq.py
│   ├── grouping_smart_algorithm_tri_seq.py
│   ├── group_seq.py
│   ├── group_smart_seq.py
├── images
│   ├── code_arch.png
│   ├── monaco.png
│   ├── privacy_leakage_project.pdf
├── __init__.py
├── logs
├── main.py
├── modules
│   ├── devicemanager.py
│   ├── device.py
│   ├── logger.py
│   ├── mongofn.py
│   ├── sniffer.py
│   └── user.py
├── pipeline.py
├── plot
│   ├── plot_q1.py
│   ├── plot_q2.py
│   ├── plot_q3.py
│   ├── plot_q4b.py
│   ├── plot_q4.py
│   ├── plot_q5.py
│   ├── plot_reconstruction.py
├── project.yml
├── pyproject.toml
├── README.md
├── reconstruction
│   ├── reconstruction_baseline.py
│   ├── reconstruction_baseline_smart.py
│   ├── reconstruction_multi_partial.py
│   ├── reconstruction_multi.py
│   ├── reconstruction_precompute_partial.py
│   └── reconstruction_user_data.py
├── sanity
│   ├── group_checker.py
│   ├── sanity_incompatible.py
│   └── sanity.py
├── services
│   ├── general.py
│   ├── __init__.py
│   ├── mongoscript.py
│   └── sl_coordinates.py
├── sumo
│   ├── generate_sniffer_data.py
│   ├── generate_user_data.py
│   ├── __init__.py
│   ├── limit_users.py
│   └── sumo_simulation.py
├── test
│   ├── test_group.py
│   ├── test_group_smart.py
│   ├── test_tracking_modified.py
│   ├── test_tracking_phases.py
│   ├── test_tracking.py
│   └── test_tracking_smart.py
└── tracking
    ├── tracking_algorithm.py
    ├── tracking_algorithm_smart.py
    ├── tracking_multi.py
    └── tracking_smart.py
```