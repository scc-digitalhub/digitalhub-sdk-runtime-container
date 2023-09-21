package it.smartcommunitylabdhub.core.repositories;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import it.smartcommunitylabdhub.core.models.entities.Task;

public interface TaskRepository extends JpaRepository<Task, String> {

    List<Task> findByFunction(String function);

    @Modifying
    @Query("DELETE FROM Task t WHERE t.project = :project ")
    void deleteByProjectName(@Param("project") String project);

}
