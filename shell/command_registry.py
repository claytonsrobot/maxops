def register_commands(shell_instance):
    """
    Registers custom commands to the given shell instance.

    Args:
        shell_instance: An instance of the cmd2 shell.
    """
    shell_instance.do_run_webapp = run_webapp
    shell_instance.do_spoof_hourly = spoof_hourly
    shell_instance.do_spoof_daily = spoof_daily
    shell_instance.do_list_exports = list_exports
    shell_instance.do_clear_exports = clear_exports
    shell_instance.do_batch = batch
    shell_instance.do_tutorial = tutorial
    shell_instance.do_query = query
