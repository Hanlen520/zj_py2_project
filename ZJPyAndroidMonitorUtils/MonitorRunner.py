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
from ZJPyAndroidMonitorUtils import MonitorUtils


# --------------------------------------------------------------
# Setup before execution
# --------------------------------------------------------------
# to be set
g_flag_print_report_all = False
g_run_num_all = '01'
g_run_time_all = 5 * MonitorUtils.g_min

g_threads = []


# --------------------------------------------------------------
# Env vars setup
# --------------------------------------------------------------
def monitor_env_vars_setup():
    set_flag_print_report()
    set_run_numbers()
    set_execution_time()

def set_flag_print_report():
    MemMonitorDumpsys.g_flag_print_report = g_flag_print_report_all
    MemMonitorProcrank.g_flag_print_report = g_flag_print_report_all

def set_run_numbers():
    MemMonitorDumpsys.g_run_num = g_run_num_all
    MemMonitorProcrank.g_run_num = g_run_num_all

def set_execution_time():
    MemMonitorDumpsys.g_run_time = g_run_time_all
    MemMonitorProcrank.g_run_time = g_run_time_all


# --------------------------------------------------------------
# Daemon thread main
# --------------------------------------------------------------
def daemon_thread_main():
    #LOOP
    while True:
        print '%s, monitor runner process is running...' %(time.strftime(MonitorUtils.g_time_format))
        time.sleep(10)


# --------------------------------------------------------------
# Build threads
# --------------------------------------------------------------
def build_daemon_thread():
    thread_name = 'monitor:daemon'
    t = threading.Thread(name=thread_name,target=daemon_thread_main)
    t.setDaemon(True)
    return t

def build_thread_mem_monitor_dumpsys():
    thread_name = 'monitor:dumpsys'
    t = threading.Thread(name=thread_name,target=MemMonitorDumpsys.mem_monitor_dumpsys_main)
    return t

def build_thread_mem_monitor_procrank():
    thread_name = 'monitor:procrank'
    t = threading.Thread(name=thread_name,target=MemMonitorProcrank.mem_monitor_procrank_main)
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
    monitor_env_vars_setup()
    
    t_daemon = build_daemon_thread()
    start_daemon_thread(t_daemon)
    
    add_thread_to_pool(build_thread_mem_monitor_dumpsys())
    add_thread_to_pool(build_thread_mem_monitor_procrank())

def monitor_runner_execution():
    if len(g_threads) == 0:
        print 'Error, there is no thread in the pool.'
        exit(1)

    start_all_threads_in_pool()
    wait_all_threads_in_pool_exit()

def monitor_runner_clearup():
    return

def monitor_runner_main():

    monitor_runner_prepare()
    monitor_runner_execution()


if __name__ == '__main__':

    monitor_runner_main()
    print 'Monitor runner DONE!'

    pass