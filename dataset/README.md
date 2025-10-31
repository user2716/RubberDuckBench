# RubberDuckBench: A Benchmark for AI Coding Assistants

<p align="center">
    <img src="../assets/logo.svg" alt="Project Logo" width="300"/>
</p>

RubberDuckBench is a multilingual benchmark of questions about code, along with detailed rubrics for evaluating ansewrs. We intend this benchmark to be a target for future research in trustworthy and correct AI coding assistants.

## Dataset

Our benchmark contains 15 questions evenly split between each language: Java, Python, and C++. Each question is contextualized in a particular project, git commit, and line number. Our artifact includes scripts to automatically clone and checkout the necessary context. Each question also includes a detailed rubric and minimal script which exemplifies the answer. 

### Repository Structure
```
RubberDuckBench/
├── dataset/                
│   ├── scripts/            # Scripts for locally cloning and checking out sample context
│   ├── java/               
│   │   ├── metadata/       # JSON files containing each sample's git repo, relevant commit, and comment location
│   │   ├── proof/          # Minimal scripts which exemplify each answer 
│   │   ├── questions/      # txt files containing each question
│   │   └── rubrics/        # JSON files containing each rubric
```

### RubberDuckBench

#### Java
1. Does the code at the end of `initializeFromLocalSearch` depend on `drawer`? 
2. What is the difference in using `HashMap` vs `singletonMap` as a parameter to `messageParams`?
3. Should I add a `null` check for `mPrefix`?
4. Do I need this `null` check for `roleInfoList`?
5. Can an exception happen here?

#### C++
1. Is there a difference between using `operator+` and `fmt::format` to concatenate the strings "[", `cManualBindings::GetLuaPlugin(tolua_S)->GetName()`, "]: ”, and  `AString(str, len)`? 
2. Can `error_code` be something other than `ECONNREFUSED` or `ECONNRESET`?
3. Is there a difference between using `m_sliceTypeStrMap.at(m_sliceType)` vs `m_sliceTypeStrMap[m_sliceType]`? 
4. Is there a difference between returning an empty `wstring` using return L""; versus using return `{}`;
5. Can `SQWLoadingPresenter::~SQWLoadingPresenter()` {} be removed?

#### Python
1. What is the difference between calling `F.cross_entropy` vs `cross_entropy`?  
2. Should I call `_compact_times()` on every `KPIset` or only cumulative `KPIsets`?
3. Should we use UTF-8 instead of ASCII as the default encoding when decoding `host`?
4. Do I need to call `deepcopy(result)` before modifying `result[DATA]`?
5. Do we need the check for `if not build_directory` ?
