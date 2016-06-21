# -*- coding: utf-8 -*-
'''
Created on 2016-6-15

@author: zhengjin

Runner to run multiple monitor scripts concurrently.

'''

import threading
import time
from ZJPyAndroidMonitorUtils import MemMonitorDumpsys
from ZJPyAndroidMonitorUtils import MemMonitorProcrank
from ZJPyAndroidMonitorUtils import CpuMonitorTop
from ZJPyAndroidMonitorUtils import MonitorUtils


# --------------------------------------------------------------
# Setup before execution
# --------------------------------------------------------------
g_pkg_name_all = ''
g_run_num_all = '01'
g_run_time_all = 5 * MonitorUtils.g_min
g_suffix_all = '%s_%s' %(MonitorUtils.g_date, g_run_num_all)


# --------------------------------------------------------------
# Env vars setup
# --------------------------------------------------------------
def monitor_runner_env_vars_setup():
    set_env_for_cpu_monitor_top()
    set_env_for_mem_monitor_dumpsys()
    set_env_for_mem_monitor_procrank()

def set_env_for_cpu_monitor_top():
    CpuMonitorTop.g_package_name = g_pkg_name_all
    CpuMonitorTop.g_run_num = g_run_num_all
    CpuMonitorTop.g_run_time = g_run_time_all
    CpuMonitorTop.g_suffix = g_suffix_all
    
    CpuMonitorTop.g_flag_top = False
    CpuMonitorTop.g_flag_top_for_pkg = True
    CpuMonitorTop.g_flag_parse_report_for_pkg = True
    
    CpuMonitorTop.g_flag_print_report = False

def set_env_for_mem_monitor_dumpsys():
    MemMonitorDumpsys.g_package_name = g_pkg_name_all
    MemMonitorDumpsys.g_run_num = g_run_num_all
    MemMonitorDumpsys.g_run_time = g_run_time_all
    MemMonitorDumpsys.g_suffix = g_suffix_all
    
    MemMonitorDumpsys.g_flag_print_report = False

def set_env_for_mem_monitor_procrank():
    MemMonitorProcrank.g_package_name = g_pkg_name_all
    MemMonitorProcrank.g_run_num = g_run_num_all
    MemMonitorProcrank.g_run_time = g_run_time_all
    MemMonitorProcrank.g_suffix = g_suffix_all

    MemMonitorProcrank.g_flag_build_report = True
    MemMonitorProcrank.g_flag_parse_report = True

    MemMonitorProcrank.g_flag_only_process = False
    MemMonitorProcrank.g_flag_only_total = False
    MemMonitorProcrank.g_flag_process_total = True
    MemMonitorProcrank.g_flag_all = False
    
    MemMonitorProcrank.g_flag_print_report = False


# --------------------------------------------------------------
# Daemon thread main
# --------------------------------------------------------------
g_daemon_thread_sleep_time = 15

def daemon_thread_main():
    #LOOP
    while True:
        print '%s, monitor runner process is running...' %(time.strftime(MonitorUtils.g_time_format))
        time.sleep(g_daemon_thread_sleep_time)


# --------------------------------------------------------------
# Build threads
# --------------------------------------------------------------
def build_daemon_thread():
    thread_name = 'monitor:daemon'
    t = threading.Thread(name=thread_name,target=daemon_thread_main)
    t.setDaemon(True)
    return t

def build_thread_mem_monitor_dumpsys():
    thread_name = 'mem:monitor:dumpsys'
    t = threading.Thread(name=thread_name,target=MemMonitorDumpsys.mem_monitor_dumpsys_main)
    return t

def build_thread_mem_monitor_procrank():
    thread_name = 'mem:monitor:procrank'
    t = threading.Thread(name=thread_name,target=MemMonitorProcrank.mem_monitor_procrank_main)
    return t

def build_thread_cpu_monitor_top():
    thread_name = 'cpu:monitor:top'
    t = threading.Thread(name=thread_name,target=CpuMonitorTop.cpu_monitor_top_main)
    return t

def add_thread_to_pool(t):
    g_threads.append(t)


# --------------------------------------------------------------
# Action on threads
# --------------------------------------------------------------
def start_daemon_thread(t_daemon):
    t_daemon.start()

def start_all_threads_in_pool():
    for t in g_threads:
        t.start()

def wait_all_threads_in_pool_exit():
    for t in g_threads:
        t.join()


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def monitor_runner_prepare():
    t_daemon = build_daemon_thread()
    start_daemon_thread(t_daemon)
    
    add_thread_to_pool(build_thread_mem_monitor_dumpsys())
    add_thread_to_pool(build_thread_mem_monitor_procrank())
    add_thread_to_pool(build_thread_cpu_monitor_top())

    monitor_runner_env_vars_setup()
    
def monitor_runner_execution():
    if len(g_threads) == 0:
        print 'Error, there is no thread in the pool.'
        exit(1)

    start_all_threads_in_pool()
    wait_all_threads_in_pool_exit()

def monitor_runner_clearup():
    # todo
    return

def monitor_runner_main():

    monitor_runner_prepare()
    monitor_runner_execution()


if __name__ == '__main__':

    g_pkg_name_all = MonitorUtils.g_package_settings
    g_run_num_all = '03'
    g_run_time_all = 5 * MonitorUtils.g_min
    g_suffix_all = '%s_%s' %(MonitorUtils.g_date, g_run_num_all)
    
    g_threads = []   # holds all running threads
    monitor_runner_main()
    del g_threads[:]
    
    print 'Monitor runner DONE!'
    pass