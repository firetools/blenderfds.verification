import_from_fds_tree(
    test=test,
    path = "/opt/FDS/FDS6/Examples/",
    compare_with_ref=False,
    run_fds = False,
    exclude_files = ("BT10m_2x2km_LS.fds", "sprinkler_many.fds"),
)
