import os

if __name__ == "__main__":
    dir_ = "logged_prompts/"
    sessions = os.listdir(dir_)
    dataset_folder = "easy_task_mini_dataset"
    datapoints = 0
    for session in sessions:
        session_dir =  os.path.join(dir_, session)
        logs_files = os.listdir(session_dir)
        inputs_step_tuple = [log.split("_") for log in logs_files if "input" in log]
        outputs_step_tuple = [log.split("_") for log in logs_files if "output" in log]
        inputs_step_tuple.sort(key=lambda x: x[1])
        outputs_step_tuple.sort(key=lambda x: x[1])
        for input_tuple, output_tuple in zip(inputs_step_tuple, outputs_step_tuple):
            input_filename = input_tuple[0]+"_"+input_tuple[1]
            output_filename = output_tuple[0]+"_"+output_tuple[1]
            input_ = os.path.join(session_dir, input_filename)
            output_ = os.path.join(session_dir, output_filename)
            with open(input_, "r") as fp:
                prompt = fp.read()
            with open(output_, "r") as fp:
                output = fp.read()
            datapoint_filename = os.path.join(dataset_folder, f"{datapoints}.txt")
            with open(datapoint_filename, "w") as fp:
                fp.write(f"#####PROMPT: {prompt}")            
                fp.write(f"#####OUTPUT: {output}")       
            datapoints+=1     
