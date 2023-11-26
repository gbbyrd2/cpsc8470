import glob
import matplotlib.pyplot as plt
import numpy as np

txt_files = glob.glob('*improved*')

txt_files.sort()

improved_avg_times = dict()
improved_avg_map_scores = dict()

# get improved results
for txt_file in txt_files:
    if 'time' in txt_file:
        num_ent_per_it = int(txt_file.split('_')[3])
        with open(txt_file, 'r') as file:
            times = file.readlines()
            for idx, time in enumerate(times):
                time = time.replace('\n', '')
                times[idx] = float(time)
            avg_time = sum(times)/len(times)
            improved_avg_times[num_ent_per_it] = avg_time
    
    if 'map' in txt_file:
        num_ent_per_it = int(txt_file.split('_')[3])
        with open(txt_file, 'r') as file:
            map_score_raw_strings = file.readlines()
            test_map_scores = map_score_raw_strings[-1]
            test_map_scores = test_map_scores.replace('\n', '')
            test_map_scores = test_map_scores.split(' ')[2:]
            for idx, score in enumerate(test_map_scores):
                test_map_scores[idx] = float(score)
            improved_avg_map_scores[num_ent_per_it] = test_map_scores

# get original results

txt_files = glob.glob('*original*')

for txt_file in txt_files:
    if 'time' in txt_file:
        with open(txt_file, 'r') as file:
            times = file.readlines()
            for idx, time in enumerate(times):
                time = time.replace('\n', '')
                times[idx] = float(time)
            avg_time = sum(times)/len(times)
            original_avg_time = avg_time
    if 'map' in txt_file:
        with open(txt_file, 'r') as file:
            map_score_raw_strings = file.readlines()
            test_map_scores = map_score_raw_strings[-1]
            test_map_scores = test_map_scores.replace('\n', '')
            test_map_scores = test_map_scores.split(' ')[2:]
            for idx, score in enumerate(test_map_scores):
                test_map_scores[idx] = float(score)
            original_avg_map_scores = test_map_scores
            
# plot the results
num_entities_per_iterations = [1]

# avg times
avg_times_list = []
avg_times_list.append(original_avg_time)
for num_ent_per_it in improved_avg_times:
    num_entities_per_iterations.append(num_ent_per_it)
    avg_times_list.append(improved_avg_times[num_ent_per_it])
    
# avg map scores
map_scores = {
    'AP10': [],
    'AP20': [],
    'AP50': [],
    'AP100': []
}
metric = [
    'AP10',
    'AP20',
    'AP50',
    'AP100',
]
for idx, score in enumerate(original_avg_map_scores):
    map_scores[metric[idx]].append(score)
    
for improved_map_score in improved_avg_map_scores.values():
    for idx, score in enumerate(improved_map_score):
        map_scores[metric[idx]].append(score)

for metric in map_scores:
    map_scores[metric] = np.array(map_scores[metric])  
        
# plot avg times
avg_times = np.array(avg_times_list)
num_entities_per_iterations = np.array(num_entities_per_iterations)
plt.figure()
plt.plot(num_entities_per_iterations, avg_times)
plt.xlabel(r'Number Entities Added Per Iteration $\phi$')
plt.ylabel('Time (s) of Expansion Algorithm')
plt.title('Improved Window Search Avg Speedup')
plt.show()

# plot avg map scores
plt.figure()

plt.plot(num_entities_per_iterations, map_scores['AP10'], label='AP10')
plt.plot(num_entities_per_iterations, map_scores['AP20'], label='AP20')
plt.plot(num_entities_per_iterations, map_scores['AP50'], label='AP50')
plt.plot(num_entities_per_iterations, map_scores['AP100'], label='AP100')
plt.xlabel(r'Number Entities Added Per Iteration $\phi$')
plt.ylabel('MAP Score of Expansion Algorithm')
plt.title('Improved Window Search Avg Performance')
plt.legend()
plt.show()




            
            