package it.smartcommunitylabdhub.core.components.infrastructure.frameworks;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.kubernetes.client.openapi.ApiException;
import io.kubernetes.client.openapi.apis.BatchV1Api;
import io.kubernetes.client.openapi.apis.CoreV1Api;
import io.kubernetes.client.openapi.models.*;
import it.smartcommunitylabdhub.core.annotations.infrastructure.FrameworkComponent;
import it.smartcommunitylabdhub.core.components.fsm.StateMachine;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunEvent;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunState;
import it.smartcommunitylabdhub.core.components.fsm.types.RunStateMachine;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.frameworks.Framework;
import it.smartcommunitylabdhub.core.components.infrastructure.runnables.K8sJobRunnable;
import it.smartcommunitylabdhub.core.components.kubernetes.K8sJobBuilderHelper;
import it.smartcommunitylabdhub.core.components.pollers.PollingService;
import it.smartcommunitylabdhub.core.components.workflows.factory.WorkflowFactory;
import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.models.builders.log.LogEntityBuilder;
import it.smartcommunitylabdhub.core.services.interfaces.LogService;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;
import it.smartcommunitylabdhub.core.utils.ErrorList;
import lombok.extern.log4j.Log4j2;
import org.apache.commons.lang3.function.TriFunction;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;

import java.util.*;
import java.util.stream.Stream;

@FrameworkComponent(framework = "k8sjob")
@Log4j2
public class K8sJobFramework implements Framework<K8sJobRunnable> {

    @Autowired
    BatchV1Api batchV1Api;

    @Autowired
    CoreV1Api coreV1Api;

    @Autowired
    PollingService pollingService;

    @Autowired
    RunStateMachine runStateMachine;

    @Autowired
    LogEntityBuilder logEntityBuilder;

    @Autowired
    LogService logService;

    @Autowired
    RunService runService;

    @Autowired
    K8sJobBuilderHelper k8sJobBuilderHelper;


    // TODO: instead of void define a Result object that have to be merged with the run from the
    // caller.
    @Override
    public void execute(K8sJobRunnable runnable) throws CoreException {
        // FIXME: DELETE THIS IS ONLY FOR DEBUG
        String threadName = Thread.currentThread().getName();

        ObjectMapper objectMapper = new ObjectMapper();

        // Log service execution initiation
        log.info("----------------- PREPARE KUBERNETES JOB ----------------");

        // Specify the Kubernetes namespace
        final String namespace = "default";

        // Generate jobName and ContainerName
        String jobName = getJobName(
                runnable.getRuntime(),
                runnable.getTask(),
                runnable.getId()
        );
        String containerName = getContainerName(
                runnable.getRuntime(),
                runnable.getTask(),
                runnable.getId()
        );

        // Create labels for job
        Map<String, String> labels = Map.of(
                "app.kubernetes.io/instance", "dhcore-" + jobName,
                "app.kubernetes.io/version", "0.0.3",
                "app.kubernetes.io/component", "job",
                "app.kubernetes.io/part-of", "dhcore-k8sjob",
                "app.kubernetes.io/managed-by", "dhcore");


        // Prepare environment variables for the Kubernetes job
        List<V1EnvVar> envVars = k8sJobBuilderHelper.getEnvV1();

        // Merge function specific envs
        runnable.getEnvs().forEach((key, value) -> envVars.add(
                new V1EnvVar().name(key).value(value)));

        // Build Container
        V1Container container = new V1Container()
                .name(containerName)
                .image(runnable.getImage())
                .command(getCommand(runnable))
                .imagePullPolicy("IfNotPresent")
                .env(envVars);

        // Create a PodSpec for the container
        V1PodSpec podSpec = new V1PodSpec()
                .containers(Collections.singletonList(container))
                .restartPolicy("Never");

        // Create a PodTemplateSpec with the PodSpec
        V1PodTemplateSpec podTemplateSpec = new V1PodTemplateSpec()
                .spec(podSpec);

        // Create the JobSpec with the PodTemplateSpec
        V1JobSpec jobSpec = new V1JobSpec()
                // .completions(1)
                // .backoffLimit(6)    // is the default value
                .template(podTemplateSpec);

        // Create the Job metadata
        V1ObjectMeta metadata = new V1ObjectMeta()
                .name(jobName)
                .labels(labels);


        // Create the V1Job object with metadata and JobSpec
        V1Job job = new V1Job()
                .metadata(metadata)
                .spec(jobSpec);

        try {
            V1Job createdJob = batchV1Api.createNamespacedJob(namespace, job, null, null, null, null);
            System.out.println("Job created: " + Objects.requireNonNull(createdJob.getMetadata()).getName());
        } catch (ApiException e) {
            // Handle exceptions here
            throw new CoreException(
                    ErrorList.RUN_JOB_ERROR.getValue(),
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR
            );
        }


        // TODO: change this part as a poller instead of a watcher using kubeclient and jobId
        // Initialize the run state machine considering current state and context
        StateMachine<RunState, RunEvent, Map<String, Object>> fsm = runStateMachine
                .create(RunState.valueOf(runnable.getState()),
                        Map.of("runId", runnable.getId()));


        // Log the initiation of Dbt Kubernetes Listener
        log.info("Dbt Kubernetes Listener [" + threadName + "] "
                + jobName
                + "@"
                + namespace);


        // Define a function with parameters
        TriFunction<String, String, StateMachine<?, ?, ?>, Void> checkJobStatus = (jName, cName, fMachine) -> {
            // Your function implementation here
            return null;
        };

        // Using the step method with explicit arguments


        pollingService.createPoller(jobName, List.of(
                WorkflowFactory.builder().step(checkJobStatus, jobName, containerName, fsm).build()
        ), 1, true);
        pollingService.startOne(jobName);

/*
        // Watch for current job events
        Watch watch = kubernetesClient.v1().events().inAnyNamespace().watch(new Watcher<Event>() {
            @Override
            public void eventReceived(Action action, Event event) {
                try {
                    // Extract involved object information from the event
                    String involvedObjectUid = event.getInvolvedObject().getUid();

                    // if event involved object is equal to the job uuid I created before then
                    // log event
                    if (jobResult.getMetadata().getUid().equals(involvedObjectUid)) {
                        EventPrinter.printEvent(event);

                        String eventJson = objectMapper.writeValueAsString(event);

                        logService.createLog(LogDTO.builder()
                                .run(runnable.getId())
                                .project(runnable.getProject())
                                .body(Map.of("content", eventJson))
                                .build());


                        if (event.getReason().equals("SuccessfulCreate")) {
                            fsm.goToState(RunState.READY);
                            fsm.goToState(RunState.RUNNING);
                        }

                        // when message is completed update run
                        if (event.getReason().equals("Completed")) {
                            fsm.goToState(RunState.COMPLETED);
                            RunDTO runDTO = runService.getRun(runnable.getId());
                            runDTO.setState(fsm.getCurrentState().name());
                            runService.updateRun(runDTO, runDTO.getId());
                        }
                    }
                } catch (Exception e) {
                    log.error(e.getMessage());
                }
            }


            @Override
            public void onClose(WatcherException cause) {
                if (cause != null) {
                    // Handle any KubernetesClientException that occurred during
                    // watch
                    log.error("An error occurred during the Kubernetes events watch: "
                            + cause.getMessage());
                } else {
                    // Handle watch closure
                    log.error("The Kubernetes events watch has been closed.");
                }
            }
        });

        // Wait until job is succeded..this is thread blocking functionality for this reason
        // every watcher is on @Async method.
        kubernetesClient.batch().v1().jobs().inNamespace(namespace)
                .withName(jobName)
                .waitUntilCondition(j -> j.getStatus().getSucceeded() != null
                        && j.getStatus().getSucceeded() > 0, 8L, TimeUnit.HOURS);

        // Get job execution logs
        String jobLogs =
                kubernetesClient.batch().v1().jobs().inNamespace(namespace)
                        .withName(jobName)
                        .getLog();

        // Write job execution logs to the log service
        logService.createLog(LogDTO.builder()
                .run(runnable.getId())
                .project(runnable.getProject())
                .body(Map.of("content", jobLogs))
                .build());


        // Close the job execution watch
        watch.close();

        // Clean up the job
        kubernetesClient.batch().v1().jobs().inNamespace(namespace)
                .withName(jobName)
                .delete();*/
    }

    // Concat command with arguments
    private List<String> getCommand(K8sJobRunnable runnable) {
        return List.of(Stream.concat(
                Stream.of(runnable.getCommand()),
                Arrays.stream(runnable.getArgs())).toArray(String[]::new));
    }

    // Generate and return job name
    private String getJobName(String runtime, String task, String id) {
        return "j" + "-" + runtime + "-" + task + "-" + id;
    }

    // Generate and return container name
    private String getContainerName(String runtime, String task, String id) {
        return "c" + "-" + runtime + "-" + task + "-" + id;
    }

}
