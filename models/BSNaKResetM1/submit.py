from subprocess import call


def submit_to_cluster(jobname, script, args):
    args = [str(arg) for arg in args]
    command = ['qsub', '-N', jobname, 'submit.sh', script] + args
    call(command)
