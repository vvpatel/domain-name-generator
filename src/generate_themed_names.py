#!/usr/bin/env python3
"""
Generate domain names with theme support (science, CS, ML, math, information retrieval).
Prioritizes English words relevant to the selected theme.
"""

import random
import sys
import os
import re
from datetime import datetime

# Add src directory to path for imports
src_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, src_dir)

from generate_domain_names import (
    score_name,
    score_english_word_like,
    score_primitive_verb_appeal,
    score_primitive_bonus,
    has_morphology_penalty,
    NamePreferences,
    is_easy_to_spell,
    CONSONANTS,
    VOWELS
)

# Theme-specific word lists
THEME_WORDS = {
    'science': [
        # Scientific concepts (removed chemistry/bio/energy terms)
        'wave', 'field', 'force', 'matter', 'mass', 'charge', 'spin', 'phase', 'state',
        'theory', 'hypothesis', 'experiment', 'observe', 'measure', 'analyze', 'test',
        'prove', 'verify', 'validate', 'discover', 'explore', 'investigate', 'study',
        'research', 'system',
        # Scientific properties
        'pure', 'precise', 'exact', 'accurate', 'rigorous', 'systematic', 'empirical',
        # Scientists (removed newton, faraday, curie)
        'darwin', 'einstein', 'tesla', 'planck', 'bohr', 'maxwell',
        'edison', 'bell', 'watt', 'euler', 'gauss', 'pascal', 'turing',
    ],
    
    'computer_science': [
        # CS concepts
        'algorithm', 'data', 'structure', 'tree', 'graph', 'node', 'edge', 'path',
        'queue', 'stack', 'heap', 'hash', 'map', 'set', 'list', 'array', 'vector',
        'matrix', 'tensor', 'bit', 'byte', 'word', 'cache', 'memory', 'register',
        'process', 'thread', 'task', 'job', 'queue', 'pool', 'buffer', 'stream',
        'parse', 'compile', 'execute', 'run', 'load', 'save', 'store', 'fetch',
        'read', 'write', 'query', 'search', 'index', 'rank', 'sort', 'filter',
        'match', 'link', 'merge', 'join', 'split', 'slice', 'extract', 'transform',
        # CS properties
        'fast', 'quick', 'efficient', 'optimal', 'scalable', 'parallel', 'concurrent',
        'async', 'sync', 'atomic', 'consistent', 'reliable', 'robust', 'secure',
        # Data science/ML training terms (CS overlap)
        'dataset', 'frame', 'series', 'pipeline', 'workflow', 'experiment', 'track',
        'version', 'reproduce', 'baseline', 'benchmark', 'evaluate', 'compare',
        # Abbreviations and acronyms
        'api', 'sdk', 'ide', 'cli', 'gui', 'os', 'cpu', 'gpu', 'ram', 'rom', 'ssd', 'hdd',
        'http', 'https', 'tcp', 'udp', 'ip', 'dns', 'cdn', 'sso', 'oauth', 'jwt', 'json',
        'xml', 'html', 'css', 'js', 'ts', 'sql', 'nosql', 'db', 'orm', 'mvc', 'mvp', 'mvvm',
        'rest', 'graphql', 'rpc', 'grpc', 'soap', 'ws', 'wss', 'ftp', 'sftp', 'ssh',
        'git', 'svn', 'ci', 'cd', 'devops', 'sre', 'qa', 'tdd', 'bdd', 'ddd',
        # Technical prefixes/suffixes
        'code', 'byte', 'bit', 'hex', 'bin', 'oct', 'dec', 'base', 'radix',
        'proto', 'meta', 'pseudo', 'semi', 'multi', 'uni', 'bi', 'tri', 'quad',
        # Programming concepts
        'func', 'method', 'class', 'obj', 'inst', 'var', 'const', 'let', 'def', 'lambda',
        'loop', 'iter', 'rec', 'cond', 'if', 'else', 'elif', 'switch', 'case', 'break',
        'cont', 'ret', 'yield', 'await', 'async', 'prom', 'then', 'catch', 'throw',
        'try', 'except', 'finally', 'raise', 'assert', 'test', 'mock', 'stub', 'spy',
        # Data structures
        'dict', 'tuple', 'enum', 'union', 'struct', 'record', 'field', 'prop', 'attr',
        'key', 'val', 'pair', 'entry', 'item', 'elem', 'cell', 'slot', 'bucket',
        # Algorithms
        'sort', 'search', 'find', 'seek', 'scan', 'traverse', 'walk', 'visit',
        'bfs', 'dfs', 'dijkstra', 'astar', 'greedy', 'dp', 'backtrack', 'divide',
        'conquer', 'merge', 'quick', 'heap', 'radix', 'count', 'bucket', 'shell',
        # System concepts
        'sys', 'proc', 'thread', 'fiber', 'coro', 'actor', 'channel', 'queue',
        'lock', 'mutex', 'sem', 'cond', 'barrier', 'latch', 'fence', 'spin',
        'deadlock', 'race', 'starv', 'livelock', 'preempt', 'schedule', 'context',
        'switch', 'yield', 'block', 'unblock', 'wake', 'sleep', 'wait', 'notify',
        # Networking
        'net', 'socket', 'port', 'host', 'client', 'server', 'peer', 'node',
        'packet', 'frame', 'segment', 'datagram', 'header', 'payload', 'trailer',
        'routing', 'switching', 'bridging', 'nat', 'vpn', 'proxy', 'gateway',
        'router', 'switch', 'hub', 'repeater', 'bridge', 'modem', 'adapter',
        # Security
        'auth', 'authz', 'encrypt', 'decrypt', 'hash', 'salt', 'pepper', 'key',
        'cert', 'pki', 'tls', 'ssl', 'cipher', 'crypto', 'sign', 'verify', 'nonce',
        # Storage
        'file', 'dir', 'folder', 'path', 'name', 'ext', 'size', 'time', 'perm',
        'read', 'write', 'append', 'trunc', 'seek', 'tell', 'flush', 'close',
        'open', 'create', 'delete', 'rename', 'move', 'copy', 'link', 'symlink',
        # Compression/encoding
        'zip', 'gzip', 'bzip', 'lzma', 'xz', 'tar', 'rar', '7z', 'encode', 'decode',
        'base64', 'base32', 'hex', 'ascii', 'utf8', 'utf16', 'utf32', 'unicode',
        # Performance
        'perf', 'bench', 'profile', 'trace', 'log', 'metric', 'stat', 'count',
        'latency', 'throughput', 'qps', 'tps', 'rps', 'ops', 'iops', 'bandwidth',
        # Testing
        'unit', 'integ', 'e2e', 'system', 'accept', 'smoke', 'regress', 'perf',
        'load', 'stress', 'chaos', 'fuzz', 'mutate', 'cover', 'assert', 'expect',
    ],
    
    'machine_learning': [
        # ML core concepts
        'model', 'train', 'learn', 'predict', 'infer', 'classify', 'cluster', 'regress',
        'embed', 'encode', 'decode', 'transform', 'normalize', 'standardize', 'scale',
        'feature', 'label', 'sample', 'batch', 'epoch', 'loss', 'error', 'metric',
        'accuracy', 'precision', 'recall', 'f1', 'score', 'rank', 'vector', 'tensor',
        'matrix', 'gradient', 'optimize', 'minimize', 'maximize', 'converge', 'diverge',
        'neural', 'network', 'layer', 'node', 'weight', 'bias', 'activation', 'output',
        'input', 'hidden', 'deep', 'shallow', 'wide', 'narrow', 'dense', 'sparse',
        # ML algorithms
        'svm', 'knn', 'kmeans', 'pca', 'rnn', 'cnn', 'lstm', 'transformer', 'bert',
        # ML properties
        'intelligent', 'adaptive', 'learned', 'trained', 'optimized', 'tuned',
        # Training ML terms
        'training', 'validate', 'test', 'split', 'fold', 'cross', 'validation',
        'overfit', 'underfit', 'regularize', 'dropout', 'early', 'stop',
        'backprop', 'forward', 'propagate', 'gradient', 'descent', 'adam', 'sgd',
        'momentum', 'learning', 'rate', 'decay', 'schedule', 'warmup',
        'pretrain', 'finetune', 'transfer', 'domain', 'adapt', 'fewshot',
        'zero', 'shot', 'prompt', 'incontext', 'instruction', 'tune',
        # Data science terms
        'dataset', 'data', 'frame', 'series', 'column', 'row', 'feature', 'target',
        'explore', 'exploratory', 'analysis', 'eda', 'visualize', 'plot', 'chart',
        'correlate', 'correlation', 'covariance', 'variance', 'std', 'dev',
        'outlier', 'anomaly', 'detect', 'clean', 'preprocess', 'impute', 'handle',
        'missing', 'encode', 'categorical', 'numerical', 'discrete', 'continuous',
        'engineer', 'selection', 'extract', 'reduce', 'dimension', 'project',
        'pipeline', 'workflow', 'experiment', 'track', 'version', 'reproduce',
        'baseline', 'benchmark', 'evaluate', 'assess', 'compare', 'ablate',
        'hyperparam', 'tune', 'grid', 'search', 'random', 'bayesian', 'opt',
        'ensemble', 'bag', 'boost', 'stack', 'blend', 'vote', 'average',
        # Abbreviations and acronyms
        'ml', 'ai', 'dl', 'nn', 'ann', 'dnn', 'cnn', 'rnn', 'lstm', 'gru', 'gan',
        'ae', 'bert', 'gpt', 't5', 'roberta', 'xlnet', 'albert', 'electra',
        'transformer', 'attention', 'selfatt', 'multihead', 'ffn', 'layernorm',
        'resnet', 'vgg', 'inception', 'mobilenet', 'efficientnet', 'yolo', 'ssd',
        'rcnn', 'fasterrcnn', 'maskrcnn', 'retinanet', 'fpn', 'unet', 'segnet',
        'svm', 'knn', 'kmeans', 'dbscan', 'hierarch', 'agglomer', 'spectral',
        'pca', 'ica', 'lda', 'tsne', 'umap', 'autoenc', 'gan', 'flow',
        'normalize', 'standardize', 'minmax', 'robust', 'quantile', 'power',
        'yeojohnson', 'boxcox', 'log', 'sqrt', 'recip', 'poly', 'spline',
        # Neural network components
        'conv', 'pool', 'maxpool', 'avgpool', 'globalpool', 'dropout', 'batchnorm',
        'layernorm', 'instancenorm', 'groupnorm', 'spectralnorm', 'weightnorm',
        'relu', 'gelu', 'elu', 'leaky', 'prelu', 'swish', 'mish', 'tanh', 'sigmoid',
        'softmax', 'logsoftmax', 'softplus', 'softsign', 'selu', 'hardtanh',
        # Optimizers
        'sgd', 'adam', 'adamw', 'rmsprop', 'adagrad', 'adadelta', 'nadam', 'adamax',
        'momentum', 'nesterov', 'lbfgs', 'adafactor', 'lamb', 'novograd', 'radam',
        # Loss functions
        'rmse', 'mape', 'smape', 'huber', 'smoothl1', 'focalloss',
        'bce', 'ce', 'nll', 'kl', 'js', 'wasserstein', 'hinge', 'squaredhinge',
        'poisson', 'cosine', 'triplet', 'contrastive', 'margin', 'arcface', 'cosface',
        # Metrics
        'acc', 'prec', 'rec', 'f1', 'fbeta', 'auc', 'roc', 'pr', 'ap', 'map',
        'iou', 'dice', 'pixelacc', 'meanacc', 'freqwacc', 'topk', 'perplexity',
        'bleu', 'rouge', 'meteor', 'cider', 'spice', 'bertscore', 'mover',
        # Data processing
        'augment', 'crop', 'flip', 'rotate', 'scale', 'shift', 'shear', 'zoom',
        'bright', 'contrast', 'saturate', 'hue', 'noise', 'blur', 'sharpen',
        'normalize', 'standardize', 'whiten', 'center', 'pca', 'zca',
        # Model types
        'supervised', 'unsupervised', 'semi', 'selfsupervised', 'weakly',
        'reinforcement', 'rl', 'qlearn', 'policy', 'actor', 'critic', 'ppo',
        'dqn', 'ddpg', 'td3', 'sac', 'trpo', 'impala', 'apex',
        # Architectures
        'residual', 'skip', 'bottleneck', 'inception', 'depthwise', 'separable',
        'dilated', 'atrous', 'deformable', 'dynamic', 'adaptive', 'learned',
        # Techniques
        'distill', 'prune', 'quantize', 'sparsify', 'compress', 'accelerate',
        'knowledge', 'transfer', 'domain', 'adapt', 'adversarial', 'robust',
        'federated', 'distributed', 'parallel', 'async', 'sync', 'gradient',
        'accumulate', 'clip', 'scale', 'mixed', 'precision', 'fp16', 'bf16',
        # Frameworks/tools
        'pytorch', 'tensorflow', 'keras', 'jax', 'flax', 'huggingface', 'transformers',
        'onnx', 'tflite', 'coreml', 'tensorrt', 'openvino', 'ncnn', 'mnn',
        'mlflow', 'wandb', 'tensorboard', 'neptune', 'comet', 'optuna', 'ray',
    ],
    
    'math': [
        # Math concepts
        'number', 'digit', 'integer', 'real', 'rational', 'irrational', 'complex',
        'prime', 'factor', 'multiple', 'divisor', 'quotient', 'remainder', 'modulo',
        'sum', 'product', 'difference', 'ratio', 'proportion', 'percent', 'fraction',
        'decimal', 'binary', 'hex', 'octal', 'base', 'exponent', 'power', 'root',
        'square', 'cube', 'log', 'ln', 'sin', 'cos', 'tan', 'angle', 'degree',
        'radian', 'pi', 'euler', 'infinity', 'limit', 'derivative', 'integral',
        'function', 'variable', 'constant', 'coefficient', 'term', 'expression',
        'equation', 'inequality', 'solve', 'compute', 'calculate', 'evaluate',
        'vector', 'matrix', 'tensor', 'scalar', 'dot', 'cross', 'norm', 'magnitude',
        'distance', 'metric', 'measure', 'space', 'dimension', 'point', 'line',
        'plane', 'curve', 'surface', 'volume', 'area', 'perimeter', 'circumference',
        # Math properties
        'exact', 'precise', 'accurate', 'rigorous', 'proof', 'theorem', 'lemma',
        'corollary', 'axiom', 'postulate', 'conjecture', 'hypothesis',
        # Mathematicians
        'euler', 'gauss', 'newton', 'leibniz', 'pascal', 'fourier', 'laplace',
        'riemann', 'hilbert', 'turing', 'godel', 'einstein',
        # Algebra
        'algebra', 'linear', 'quadratic', 'cubic', 'quartic', 'polynomial', 'monomial',
        'binomial', 'trinomial', 'factor', 'expand', 'simplify', 'substitute',
        'eliminate', 'reduce', 'combine', 'distribute', 'commute', 'associate',
        # Calculus
        'calc', 'deriv', 'integral', 'diff', 'diffeq', 'ode', 'pde', 'limit', 'continu',
        'differentiable', 'smooth', 'analytic', 'taylor', 'maclaurin', 'series',
        'converge', 'diverge', 'radius', 'interval', 'domain', 'range', 'codomain',
        # Geometry
        'geo', 'euclid', 'non', 'hyperbolic', 'elliptic', 'spherical', 'projective',
        'affine', 'topology', 'manifold', 'surface', 'curve', 'geodesic', 'metric',
        'triangle', 'square', 'circle', 'ellipse', 'parabola', 'hyperbola', 'polygon',
        'pentagon', 'hexagon', 'octagon', 'polyhedron', 'tetrahedron', 'cube', 'dodeca',
        # Statistics
        'stat', 'prob', 'random', 'sample', 'pop', 'mean', 'median', 'mode', 'std',
        'var', 'cov', 'corr', 'skew', 'kurt', 'quartile', 'percentile', 'iqr',
        'distrib', 'normal', 'gaussian', 'uniform', 'expo', 'poisson', 'binomial',
        'bernoulli', 'gamma', 'beta', 'chi', 'student', 'fisher', 't', 'z',
        # Number theory
        'gcd', 'lcm', 'mod', 'congru', 'divis', 'prime', 'composite', 'factor',
        'euclid', 'fermat', 'wilson', 'chinese', 'remainder', 'euler', 'totient',
        'mobius', 'riemann', 'zeta', 'dirichlet', 'l', 'function', 'analytic',
        # Linear algebra
        'lin', 'alg', 'vector', 'matrix', 'tensor', 'scalar', 'dot', 'cross', 'outer',
        'transpose', 'inverse', 'det', 'trace', 'rank', 'null', 'span', 'basis',
        'orthogonal', 'orthonormal', 'eigen', 'value', 'vector', 'svd', 'qr', 'lu',
        'cholesky', 'schur', 'jordan', 'canonical', 'form', 'diagonal', 'triangular',
        # Discrete math
        'discrete', 'combinatorics', 'permute', 'combine', 'factorial', 'choose',
        'pascal', 'triangle', 'fibonacci', 'catalan', 'stirling', 'bell', 'partition',
        'graph', 'theory', 'tree', 'forest', 'cycle', 'path', 'walk', 'trail',
        'connected', 'component', 'bipartite', 'planar', 'coloring', 'matching',
        # Set theory
        'set', 'union', 'intersect', 'diff', 'complement', 'subset', 'superset',
        'power', 'cartesian', 'product', 'relation', 'function', 'map', 'inject',
        'surject', 'biject', 'cardinal', 'ordinal', 'countable', 'uncountable',
        # Logic
        'logic', 'proposition', 'predicate', 'quantifier', 'forall', 'exists',
        'and', 'or', 'not', 'implies', 'iff', 'tautology', 'contradiction',
        'satisfiable', 'valid', 'sound', 'complete', 'consistent', 'decidable',
        # Abstract algebra
        'group', 'ring', 'field', 'module', 'vector', 'space', 'algebra', 'lie',
        'homomorphism', 'isomorphism', 'automorphism', 'kernel', 'image', 'quotient',
        'subgroup', 'normal', 'cyclic', 'abelian', 'symmetric', 'alternating',
        # Topology
        'topology', 'topological', 'space', 'open', 'closed', 'compact', 'connected',
        'path', 'connected', 'simply', 'manifold', 'homeomorphism', 'homotopy',
        'fundamental', 'group', 'homology', 'cohomology', 'betti', 'euler', 'char',
        # Analysis
        'analysis', 'real', 'complex', 'measure', 'theory', 'lebesgue', 'borel',
        'sigma', 'algebra', 'measurable', 'function', 'integral', 'derivative',
        'fourier', 'transform', 'laplace', 'z', 'wavelet', 'hilbert', 'space',
        # Numerical methods
        'numerical', 'approximate', 'interpolate', 'extrapolate', 'extrap',
        'newton', 'raphson', 'secant', 'bisect', 'regula', 'falsi', 'fixed', 'point',
        'runge', 'kutta', 'euler', 'method', 'trapezoid', 'simpson', 'gauss',
        'quadrature', 'monte', 'carlo', 'finite', 'difference', 'element',
        # Symbols and notation
        'sigma', 'sum', 'pi', 'prod', 'integral', 'partial', 'nabla', 'del',
        'infinity', 'infty', 'forall', 'exists', 'in', 'notin', 'subset', 'superset',
        'union', 'cup', 'intersect', 'cap', 'emptyset', 'emptyset', 'element',
    ],
    
    'information_retrieval': [
        # IR core concepts
        'search', 'query', 'index', 'rank', 'score', 'match', 'retrieve', 'fetch',
        'find', 'seek', 'locate', 'discover', 'extract', 'parse', 'tokenize',
        'stem', 'lemmatize', 'normalize', 'filter', 'sort', 'order', 'arrange',
        'organize', 'categorize', 'classify', 'cluster', 'group', 'segment',
        'document', 'text', 'term', 'word', 'phrase', 'sentence', 'paragraph',
        'corpus', 'collection', 'dataset', 'repository', 'archive', 'library',
        'catalog', 'directory', 'registry', 'database', 'store', 'cache',
        # IR metrics
        'precision', 'recall', 'f1', 'map', 'ndcg', 'mrr', 'accuracy', 'relevance',
        # IR techniques
        'tfidf', 'bm25', 'cosine', 'jaccard', 'euclidean', 'manhattan', 'hamming',
        'levenshtein', 'edit', 'distance', 'similarity', 'dissimilarity',
        'vector', 'embedding', 'semantic', 'syntactic', 'lexical',
        # IR properties
        'relevant', 'precise', 'accurate', 'fast', 'efficient', 'scalable',
        'comprehensive', 'complete', 'exhaustive', 'thorough',
        # Additional IR terms
        'lookup', 'scan', 'browse', 'navigate', 'traverse', 'iterate', 'enumerate',
        'aggregate', 'merge', 'join', 'union', 'intersect', 'diff', 'subtract',
        'transform', 'map', 'reduce', 'fold', 'unfold', 'flatten', 'nest',
        'encode', 'decode', 'compress', 'decompress', 'serialize', 'deserialize',
        'hash', 'digest', 'checksum', 'fingerprint', 'signature', 'token',
        'prefix', 'suffix', 'substring', 'subsequence', 'ngram', 'bigram', 'trigram',
        'inverted', 'forward', 'backward', 'bidirectional', 'multilingual',
        'relevance', 'ranking', 'scoring', 'weighting', 'boosting', 'penalizing',
        'rerank', 'refine', 'optimize', 'tune', 'calibrate', 'adjust',
        # Abbreviations
        'ir', 'se', 'seo', 'sem', 'serp', 'qbe', 'qbs', 'qbd', 'qbt', 'qbf',
        'nlp', 'ner', 'pos', 'dep', 'parse', 'tree', 'constituency', 'dependency',
        # Search types
        'fulltext', 'boolean', 'fuzzy', 'wildcard', 'regex', 'phrase', 'proximity',
        'field', 'range', 'facet', 'filter', 'boost', 'function', 'script',
        # Indexing
        'index', 'inverted', 'forward', 'posting', 'list', 'skip', 'pointer',
        'term', 'doc', 'freq', 'tf', 'df', 'idf', 'tfidf', 'bm25', 'lm', 'dirichlet',
        'jelinek', 'mercer', 'absolute', 'discount', 'laplace', 'lidstone',
        # Ranking models
        'vsm', 'vector', 'space', 'probabilistic', 'language', 'model', 'lm',
        'unigram', 'bigram', 'trigram', 'n', 'gram', 'markov', 'chain', 'hidden',
        'hmm', 'crf', 'conditional', 'random', 'field', 'maximum', 'entropy',
        'me', 'svm', 'rank', 'learning', 'to', 'rank', 'ltr', 'lambdamart',
        'ranknet', 'listnet', 'adrank', 'xendcg', 'ndcg', 'map', 'mrr', 'mrr',
        # Query processing
        'query', 'parse', 'expand', 'rewrite', 'reformulate', 'translate',
        'intent', 'classify', 'segment', 'decompose', 'federate', 'aggregate',
        'fusion', 'combine', 'merge', 'interleave', 'diversify', 'rerank',
        # Text processing
        'tokenize', 'segment', 'normalize', 'lowercase', 'uppercase', 'casefold',
        'stem', 'lemmatize', 'pos', 'tag', 'chunk', 'parse', 'ner', 'entity',
        'recognize', 'extract', 'link', 'resolve', 'coreference', 'resolve',
        'stopword', 'remove', 'filter', 'prune', 'trim', 'clean', 'sanitize',
        # Embeddings
        'embed', 'embedding', 'vector', 'dense', 'sparse', 'bow', 'tfidf',
        'word2vec', 'fasttext', 'glove', 'elmo', 'bert', 'roberta', 'xlnet',
        'sentence', 'transformer', 'universal', 'sentence', 'encoder', 'use',
        'sbert', 'simcse', 'contrastive', 'learning', 'triplet', 'loss',
        # Similarity measures
        'cosine', 'dot', 'product', 'euclidean', 'manhattan', 'chebyshev',
        'minkowski', 'hamming', 'jaccard', 'dice', 'overlap', 'sorensen',
        'levenshtein', 'edit', 'distance', 'lcs', 'longest', 'common', 'subsequence',
        'dtw', 'dynamic', 'time', 'warping', 'kl', 'divergence', 'js', 'jensen',
        'shannon', 'wasserstein', 'earth', 'mover', 'emd', 'bhattacharyya',
        # Evaluation metrics
        'precision', 'recall', 'f1', 'fbeta', 'accuracy', 'error', 'rate',
        'map', 'mean', 'average', 'precision', 'ndcg', 'normalized', 'discounted',
        'cumulative', 'gain', 'mrr', 'reciprocal', 'rank', 'dcg', 'idcg',
        'rr', 'reciprocal', 'rank', 'ap', 'average', 'precision', 'p', 'at', 'k',
        'r', 'at', 'k', 'mrr', 'ndcg', 'at', 'k', 'err', 'expected', 'reciprocal',
        'rank', 'rbp', 'rank', 'biased', 'precision', 'inst', 'instantaneous',
        # Search engines
        'lucene', 'solr', 'elasticsearch', 'sphinx', 'xapian', 'whoosh', 'tantivy',
        'meilisearch', 'typesense', 'vespa', 'opensearch', 'algolia', 'swiftype',
        # Query languages
        'sql', 'nosql', 'sparql', 'cypher', 'gremlin', 'graphql', 'dsl', 'query',
        'lucene', 'query', 'syntax', 'boolean', 'query', 'parser', 'ast',
        # Index structures
        'b', 'tree', 'bplus', 'lsm', 'log', 'structured', 'merge', 'sst', 'sorted',
        'string', 'table', 'bloom', 'filter', 'cuckoo', 'hash', 'trie', 'radix',
        'suffix', 'array', 'tree', 'fm', 'index', 'wavelet', 'matrix', 'compressed',
        # Compression
        'compress', 'deflate', 'gzip', 'bzip', 'lz4', 'snappy', 'zstd', 'lzma',
        'delta', 'encoding', 'variable', 'byte', 'encoding', 'vbyte', 'varint',
        'gamma', 'delta', 'elias', 'golomb', 'rice', 'huffman', 'arithmetic',
        # Distributed search
        'distributed', 'shard', 'replica', 'primary', 'secondary', 'leader',
        'follower', 'coordinator', 'router', 'gateway', 'proxy', 'load', 'balance',
        'consistent', 'hashing', 'ring', 'gossip', 'protocol', 'raft', 'paxos',
    ],
    
    'scale': [
        # Size and magnitude
        'big', 'large', 'vast', 'huge', 'massive', 'immense', 'enormous', 'giant',
        'mega', 'macro', 'grand', 'major', 'max', 'peak', 'summit', 'apex', 'zenith',
        'titan', 'colossal', 'towering', 'monumental', 'mighty', 'powerful',
        # Depth
        'deep', 'profound', 'bottomless', 'abyss', 'core', 'center', 'heart', 'essence',
        'root', 'base', 'foundation', 'bedrock', 'depths',
        # Breadth and expanse
        'wide', 'broad', 'expansive', 'extensive', 'comprehensive', 'full', 'complete',
        'span', 'reach', 'range', 'scope', 'extent', 'scale', 'magnitude',
        # Height and elevation
        'high', 'tall', 'elevated', 'lofty', 'towering', 'sky', 'cloud', 'peak',
        'summit', 'pinnacle', 'crest', 'ridge', 'height',
        # Infinity and boundlessness
        'infinite', 'endless', 'boundless', 'limitless', 'eternal', 'perpetual',
        'unlimited', 'unbounded', 'immeasurable', 'incalculable',
        # Volume and capacity
        'volume', 'capacity', 'bulk', 'mass', 'weight', 'density', 'magnitude',
        # Scale-related concepts
        'scale', 'magnitude', 'scope', 'range', 'span', 'reach', 'extent', 'breadth',
        'width', 'depth', 'height', 'length', 'dimension', 'measure',
        # Size synonyms
        'gigantic', 'titanic', 'mammoth', 'gargantuan', 'leviathan', 'behemoth',
        'jumbo', 'king', 'size', 'oversized', 'outsize', 'overscale', 'supersize',
        'mega', 'giga', 'tera', 'peta', 'exa', 'zetta', 'yotta', 'kilo', 'hecto',
        'deca', 'deci', 'centi', 'milli', 'micro', 'nano', 'pico', 'femto', 'atto',
        # Magnitude terms
        'magnitude', 'amplitude', 'intensity', 'strength', 'force', 'power', 'energy',
        'momentum', 'velocity', 'speed', 'rate', 'frequency', 'density', 'concentration',
        # Extent terms
        'extent', 'scope', 'span', 'reach', 'range', 'breadth', 'width', 'length',
        'stretch', 'spread', 'stretch', 'span', 'coverage', 'domain', 'territory',
        'expanse', 'stretch', 'sweep', 'span', 'reach', 'range', 'scope', 'extent',
        # Comprehensive terms
        'comprehensive', 'complete', 'full', 'total', 'entire', 'whole', 'all',
        'exhaustive', 'thorough', 'complete', 'full', 'total', 'entire', 'whole',
        'universal', 'global', 'worldwide', 'omnipresent', 'ubiquitous', 'pervasive',
        # Depth terms
        'deep', 'profound', 'bottomless', 'abyssal', 'abysmal', 'unfathomable',
        'immeasurable', 'infinite', 'endless', 'boundless', 'limitless', 'eternal',
        'core', 'center', 'heart', 'essence', 'soul', 'spirit', 'kernel', 'nucleus',
        'root', 'base', 'foundation', 'bedrock', 'ground', 'basis', 'fundamental',
        # Height terms
        'high', 'tall', 'elevated', 'lofty', 'towering', 'soaring', 'sky', 'high',
        'cloud', 'peak', 'summit', 'pinnacle', 'crest', 'ridge', 'height', 'altitude',
        'elevation', 'zenith', 'apex', 'acme', 'climax', 'culmination', 'peak',
        # Width terms
        'wide', 'broad', 'expansive', 'spacious', 'roomy', 'capacious', 'voluminous',
        'extensive', 'sweeping', 'vast', 'immense', 'enormous', 'gigantic', 'colossal',
        # Volume terms
        'volume', 'capacity', 'bulk', 'mass', 'weight', 'density', 'magnitude', 'size',
        'quantity', 'amount', 'measure', 'extent', 'scope', 'range', 'span', 'reach',
        # Boundless terms
        'infinite', 'endless', 'boundless', 'limitless', 'eternal', 'perpetual',
        'unlimited', 'unbounded', 'immeasurable', 'incalculable', 'inexhaustible',
        'unfathomable', 'unlimited', 'unrestricted', 'unconstrained', 'unfettered',
        # Maximum terms
        'max', 'maximum', 'peak', 'summit', 'apex', 'zenith', 'acme', 'climax',
        'culmination', 'pinnacle', 'top', 'height', 'extreme', 'ultimate', 'supreme',
        # Scale prefixes
        'mega', 'macro', 'giga', 'tera', 'peta', 'exa', 'zetta', 'yotta', 'kilo',
        'hecto', 'deca', 'deci', 'centi', 'milli', 'micro', 'nano', 'pico', 'femto',
        'atto', 'zepto', 'yocto', 'super', 'ultra', 'hyper', 'meta', 'omni', 'pan',
        # Measure terms
        'measure', 'metric', 'gauge', 'scale', 'ruler', 'yardstick', 'benchmark',
        'standard', 'norm', 'criterion', 'yardstick', 'touchstone', 'barometer',
        # Dimension terms
        'dimension', 'aspect', 'facet', 'side', 'angle', 'perspective', 'viewpoint',
        'view', 'outlook', 'standpoint', 'position', 'stance', 'attitude', 'approach',
    ],
}

# Base English words (always included)
BASE_WORDS = [
    'seek', 'find', 'index', 'rank', 'score', 'match', 'link', 'fetch', 'query', 'search',
    'trace', 'track', 'scan', 'probe', 'dig', 'mine', 'map', 'parse', 'extract', 'retrieve',
    'discover', 'explore', 'navigate', 'filter', 'sort', 'merge', 'join', 'split', 'slice',
    'vector', 'matrix', 'tensor', 'graph', 'tree', 'node', 'edge', 'path', 'route',
    'core', 'base', 'hub', 'mesh', 'grid', 'net', 'web', 'flow', 'wave', 'pulse',
    'beam', 'ray', 'arc', 'peak', 'ridge', 'valley', 'point', 'line', 'plane',
    'field', 'range', 'scope', 'span', 'width', 'depth', 'height', 'scale',
    'smart', 'wise', 'quick', 'fast', 'rapid', 'swift', 'instant', 'real', 'live',
    'pure', 'true', 'clear', 'bright', 'sharp', 'deep', 'wide', 'vast', 'exact',
    'precise', 'pascal', 'turing', 'euler', 'gauss', 'darwin', 'einstein',
]

def has_single_letter_affix(name: str) -> bool:
    """Check if name has a single-letter prefix or suffix (e.g., 'queryq', 'xfind', 'queryx', 'findex')."""
    if len(name) < 3:
        return False
    
    name_lower = name.lower()
    
    # Check for single-letter suffix (e.g., 'queryq', 'queryx', 'findex')
    # Problematic single letters that rarely appear alone: q, x, z, j, k, w, y
    problematic_single_letters = ['q', 'x', 'z', 'j', 'k', 'w', 'y']
    last_char = name_lower[-1]
    
    if last_char in problematic_single_letters:
        # If ends with problematic single letter and has at least 4 chars, likely a suffix
        if len(name_lower) >= 4:
            # Check if second-to-last is a consonant (suggests word + single letter)
            if name_lower[-2] in CONSONANTS:
                return True
            # Also check if it's a common word pattern like "query" + "q"
            # If the name minus last char is a valid-looking word (has vowels)
            base = name_lower[:-1]
            if len(base) >= 3 and any(c in VOWELS for c in base):
                return True
    
    # Check for single-letter prefix (e.g., 'xfind', 'qsearch')
    first_char = name_lower[0]
    if first_char in problematic_single_letters and len(name_lower) >= 4:
        # Check if second char is a consonant (suggests single letter + word)
        if name_lower[1] in CONSONANTS:
            # Check if the rest looks like a word (has vowels)
            rest = name_lower[1:]
            if any(c in VOWELS for c in rest):
                return True
    
    return False

def has_bad_brand_patterns(name: str) -> bool:
    """
    Check for patterns that make names look auto-generated or weak as brands.
    Based on feedback: avoid suffix spam, metric salad, letter-swapped variants, model references.
    
    Returns True if name should be filtered out (bad brand pattern detected).
    """
    name_lower = name.lower()
    
    # Pattern 1: Suffix spam (-ic, -al, -ed, -er, -ly, -ive, -ize, -tion, -sion, etc.)
    # Examples: rankic, dataal, nodeer, termic, lossed, biasly, joinly, stemer, plotic,
    #           linkive, indexive, rankive, queryive, matchive, rankize, indexize
    problematic_suffixes = ['ic', 'al', 'ed', 'er', 'ly', 'ive', 'ize', 'tion', 'sion', 
                           'ast', 'sem', 'est', 'able', 'ible', 'ment', 'ance', 'ence']
    
    # Valid English words that end in these suffixes (don't filter these)
    valid_words_with_suffixes = {
        'filter', 'finder', 'seeker', 'ranker', 'scorer', 'matcher', 'linker',
        'parser', 'extractor', 'retriever', 'searcher', 'indexer', 'sorter',
        'merger', 'joiner', 'splitter', 'slicer', 'cutter', 'trimmer', 'cleaner',
        'reader', 'writer', 'loader', 'saver', 'storer', 'fetcher', 'querier',
        'scanner', 'walker', 'visitor', 'tracer', 'tracker', 'prober', 'digger',
        'miner', 'discoverer', 'explorer', 'navigator', 'traverser', 'ranking',
        'querying', 'indexing', 'loading', 'joining', 'folding', 'triming', 'linking'
    }
    
    # If it's a valid English word, don't filter (but still check other patterns below)
    # Note: We check valid_words first, but still need to check other patterns
    is_valid_word = name_lower in valid_words_with_suffixes
    
    if not is_valid_word:
        # Check if name ends with these suffixes and the root word is a common technical term
        # This catches cases like "rankic" (rank + ic), "dataal" (data + al), etc.
        for suffix in problematic_suffixes:
            if name_lower.endswith(suffix) and len(name_lower) >= 5:
                # Extract the root (everything before the suffix)
                root = name_lower[:-len(suffix)]
                
                # If root is a common technical word, this is likely suffix spam
                common_tech_roots = [
                    'rank', 'data', 'node', 'term', 'loss', 'scan', 'fast', 'bias', 'join',
                    'stem', 'plot', 'shot', 'wide', 'test', 'fold', 'zero', 'word', 'code',
                    'byte', 'bit', 'file', 'path', 'link', 'edge', 'tree', 'list', 'map',
                    'set', 'hash', 'key', 'val', 'pair', 'item', 'elem', 'cell', 'slot',
                    'sort', 'search', 'find', 'seek', 'walk', 'visit', 'read',
                    'write', 'load', 'save', 'store', 'fetch', 'query', 'index', 'match',
                    'merge', 'split', 'slice', 'cut', 'trim', 'clean', 'adam', 'bert',
                    'trace', 'track', 'mine', 'scale', 'parse', 'sparse', 'rerank', 'cache',
                    'filter'
                ]
                
                if root in common_tech_roots:
                    return True  # Bad: rankic, dataal, nodeer, adamer, linkive, indexive, etc.
                
                # Also check if root + suffix creates an awkward combination
                # e.g., "lossed" (loss + ed), "berter" (bert + er), "linkive" (link + ive)
                if len(root) >= 3 and root[-1] in CONSONANTS:
                    # If root ends in consonant and suffix starts with vowel/consonant, it's likely awkward
                    if suffix in ['ed', 'er', 'ic', 'al', 'ly', 'ive', 'ize']:
                        # Additional check: if the combination looks forced
                        if root[-1] in 'rst' and suffix in ['ed', 'er']:
                            return True  # e.g., "lossed", "berter"
                        if root[-1] in 'mn' and suffix in ['ic', 'al']:
                            return True  # e.g., "termic", "dataal"
                        if root[-1] in 'k' and suffix in ['ive', 'ize']:
                            return True  # e.g., "linkive", "rankize"
                        if root[-1] in 'x' and suffix in ['ive', 'ize']:
                            return True  # e.g., "indexive", "indexize"
                
                # Filter made-up suffix combinations like -tion, -sion, -ast, -sem, -est
                # These are almost always auto-generated looking
                if suffix in ['tion', 'sion', 'ast', 'sem', 'est']:
                    if root in common_tech_roots or (len(root) >= 3 and root[-1] in CONSONANTS):
                        return True  # e.g., "linktion", "linksion", "linkast", "linksem", "linkest"
    
    # Pattern 2: Metric salad (evaluation metrics)
    # Examples: smape, pcascore, scoreauc, scoremse, scoremae, scoref1, scorekl, listnet, ranknet
    metric_terms = [
        'smape', 'mape', 'mae', 'mse', 'rmse', 'f1', 'fbeta', 'auc', 'roc', 'pr',
        'ap', 'map', 'ndcg', 'mrr', 'dcg', 'idcg', 'err', 'rbp', 'iou', 'dice',
        'bleu', 'rouge', 'meteor', 'cider', 'spice', 'bertscore', 'mover',
        'pcascore', 'scoreauc', 'scoremse', 'scoremae', 'scoref1', 'scorekl',
        'scoremap', 'scorendcg', 'scoremrr', 'listnet', 'ranknet', 'adrank'
    ]
    
    if name_lower in metric_terms:
        return True
    
    # Check if name contains metric terms
    for metric in metric_terms:
        if metric in name_lower and len(metric) >= 3:
            return True
    
    # Pattern 3: Letter-swapped score/index/query names (strengthened)
    # Examples: sscore, rscore, scorei, indexi, queryi, wquery, oindex
    # But NOT valid words like "parser", "ranker", "matcher"
    base_words = ['score', 'rank', 'index', 'query', 'search', 'parse', 'match']
    for base in base_words:
        if len(name_lower) > len(base):
            # Single letter prefix (e.g., sscore, rscore, wquery, oindex)
            if name_lower.startswith(base) and len(name_lower) == len(base) + 1:
                # Don't filter if it's a valid word (e.g., "parser" is valid)
                if name_lower not in valid_words_with_suffixes:
                    if name_lower[-1].isalpha():
                        return True  # e.g., "scorei", "indexi"
            # Single letter suffix (e.g., sscore, rscore)
            elif name_lower.endswith(base) and len(name_lower) == len(base) + 1:
                # Don't filter if it's a valid word
                if name_lower not in valid_words_with_suffixes:
                    if name_lower[0].isalpha():
                        return True  # e.g., "sscore", "rscore", "wquery", "oindex"
    
    # Pattern 4: Over-specified model references (will age badly)
    # Examples: bertic, berted, adamer, baset5, basetf, vaescore
    model_terms = [
        'bert', 'roberta', 'albert', 'electra', 'gpt', 't5', 't3', 't2', 't1',
        'vae', 'gan', 'lstm', 'gru', 'cnn', 'rnn', 'transformer', 'attention', 'tf'
    ]
    
    # Check if name contains model terms in a way that anchors to specific tech
    for model in model_terms:
        if model in name_lower:
            # If it's just the model name, that's OK (e.g., "bert" as a primitive)
            # But if it's combined with suffixes or other words, it's over-specified
            if name_lower != model:
                # Check for combinations like "bertic", "berted", "adamer", "baset5", "basetf"
                if (name_lower.startswith(model) and len(name_lower) > len(model)) or \
                   (name_lower.endswith(model) and len(name_lower) > len(model)) or \
                   (f'{model}score' in name_lower) or (f'base{model}' in name_lower) or \
                   (f'{model}base' in name_lower):
                    return True  # Over-specified model reference
    
    return False


def has_awkward_vowel_ending(name: str) -> bool:
    """Check if name ends with awkward vowel-vowel patterns like eive, eing, eed, eest."""
    name_lower = name.lower()
    if len(name_lower) < 4:
        return False
    
    # Pattern 1: Ends with 'ed' where the character before is 'e' (like scoreed, rankeed)
    # This creates awkward "e + ed" pattern
    if len(name_lower) >= 3:
        if name_lower.endswith('ed'):
            # Check if character before 'ed' is 'e' (like scoreed, rankeed)
            if len(name_lower) >= 3 and name_lower[-3] == 'e':
                return True
    
    # Pattern 1b: Ends with 'est' where the character before is 'e' (like scoreest, rankeest)
    # This creates awkward "e + est" pattern
    if len(name_lower) >= 4:
        if name_lower.endswith('est'):
            # Check if character before 'est' is 'e' (like scoreest, rankeest)
            if name_lower[-4] == 'e':
                return True
    
    # Pattern 2: Ends with 'ive' or 'ing' where the character before is a vowel
    # Examples: eive, aive, oive, uive, eing, aing, oing, uing
    if len(name_lower) >= 4:
        if name_lower.endswith('ive'):
            # Check if character before 'ive' is a vowel (like eive, aive, oive, uive)
            if name_lower[-4] in VOWELS:
                return True
            # Also check if there's a vowel-vowel sequence in the last 5 chars
            last_5 = name_lower[-5:] if len(name_lower) >= 5 else name_lower
            for i in range(len(last_5) - 1):
                if last_5[i] in VOWELS and last_5[i+1] in VOWELS:
                    return True
        if name_lower.endswith('ing'):
            # Check if character before 'ing' is a vowel (like eing, aing, oing, uing)
            if name_lower[-4] in VOWELS:
                return True
            # Also check if there's a vowel-vowel sequence in the last 5 chars
            last_5 = name_lower[-5:] if len(name_lower) >= 5 else name_lower
            for i in range(len(last_5) - 1):
                if last_5[i] in VOWELS and last_5[i+1] in VOWELS:
                    return True
    
    # Pattern 3: Three or more consecutive vowels anywhere in the name (e.g., 'treeer', 'aiiee')
    if len(name_lower) >= 3:
        # Check for 3+ consecutive vowels anywhere in the name
        consecutive_vowels = 0
        for char in name_lower:
            if char in VOWELS:
                consecutive_vowels += 1
                if consecutive_vowels >= 3:
                    return True
            else:
                consecutive_vowels = 0
    
    # Pattern 4: Vowel-vowel-consonant-vowel at end (like eive, aive)
    # This catches cases where two vowels are followed by consonant then vowel
    if len(name_lower) >= 4:
        last_4 = name_lower[-4:]
        # Pattern: V V C V (vowel, vowel, consonant, vowel ending)
        if (last_4[0] in VOWELS and last_4[1] in VOWELS and 
            last_4[2] in CONSONANTS and last_4[3] in VOWELS):
            return True
    
    return False

def get_theme_words(theme: str) -> list:
    """Get words for a specific theme."""
    theme_lower = theme.lower()
    words = BASE_WORDS.copy()
    
    if theme_lower in THEME_WORDS:
        words.extend(THEME_WORDS[theme_lower])
    
    # Filter by length and remove awkward vowel endings (length filtering happens in generate_themed_names)
    words = [w for w in words if not has_awkward_vowel_ending(w)]
    return list(set(words))  # Remove duplicates

def score_theme_relevance(name: str, theme: str) -> float:
    """Score how relevant a name is to the selected theme."""
    score = 0.0
    name_lower = name.lower()
    theme_lower = theme.lower()
    
    if theme_lower not in THEME_WORDS:
        return 0.0
    
    theme_words = THEME_WORDS[theme_lower]
    
    # PENALIZE chemistry/bio/energy sounding names (rank lower) - STRONG PENALTY
    chemistry_bio_energy_patterns = [
        'atom', 'molecule', 'particle', 'protein', 'gene', 'cell', 'tissue', 'organ',
        'enzyme', 'catalyst', 'reaction', 'compound', 'element', 'ion', 'bond',
        'energy', 'power', 'fuel', 'battery', 'charge', 'current', 'voltage',
        'chem', 'organic', 'inorganic', 'synthetic', 'polymer', 'crystal',
    ]
    
    for pattern in chemistry_bio_energy_patterns:
        if pattern in name_lower:
            score -= 80  # Strong penalty for chemistry/bio/energy (was 40)
            break
    
    # BOOST math/CS/ML/IR sounding names (rank higher) - STRONG BOOST
    math_cs_ml_ir_patterns = [
        # Math
        'calc', 'compute', 'solve', 'vector', 'matrix', 'tensor', 'prime', 'factor',
        'metric', 'function', 'variable', 'constant', 'equation', 'formula', 'theorem',
        # CS
        'code', 'data', 'algo', 'struct', 'tree', 'graph', 'node', 'hash', 'cache',
        'stack', 'queue', 'heap', 'list', 'set', 'map', 'array', 'bit', 'byte',
        # ML
        'learn', 'train', 'model', 'neural', 'embed', 'predict', 'classify', 'cluster',
        'gradient', 'optimize', 'loss', 'error', 'feature', 'label',
        # IR
        'search', 'query', 'index', 'rank', 'retrieve', 'match', 'score', 'parse',
        'extract', 'filter', 'sort', 'token', 'term', 'document', 'corpus',
    ]
    
    for pattern in math_cs_ml_ir_patterns:
        if pattern in name_lower:
            score += 100  # Strong boost for math/CS/ML/IR (was 50)
            break
    
    # Full match with theme word (but check if it's chemistry/bio first)
    if name_lower in theme_words:
        # Check if it's a chemistry/bio word - if so, reduce the boost
        is_chemistry_bio = any(pattern in name_lower for pattern in chemistry_bio_energy_patterns)
        if is_chemistry_bio:
            score += 20  # Reduced boost for chemistry/bio words
        else:
            score += 100  # Full boost for other theme words
    
    # Contains theme word
    for word in theme_words:
        if len(word) >= 4 and word in name_lower:
            score += 50
            break  # Only count one major match
    
    # Check for theme-specific patterns
    if theme_lower == 'machine_learning':
        ml_patterns = ['learn', 'train', 'model', 'neural', 'embed', 'vector', 'tensor']
        for pattern in ml_patterns:
            if pattern in name_lower:
                score += 30
    
    elif theme_lower == 'information_retrieval':
        ir_patterns = ['search', 'query', 'index', 'rank', 'retrieve', 'match', 'score']
        for pattern in ir_patterns:
            if pattern in name_lower:
                score += 30
    
    elif theme_lower == 'math':
        math_patterns = ['calc', 'compute', 'solve', 'vector', 'matrix', 'tensor', 'prime']
        for pattern in math_patterns:
            if pattern in name_lower:
                score += 30
    
    elif theme_lower == 'computer_science':
        cs_patterns = ['code', 'data', 'algo', 'struct', 'tree', 'graph', 'node', 'hash']
        for pattern in cs_patterns:
            if pattern in name_lower:
                score += 30
    
    elif theme_lower == 'science':
        # For science theme, prioritize math/CS/ML/IR over chemistry/bio
        math_cs_patterns = ['theory', 'compute', 'solve', 'vector', 'matrix', 'tensor', 
                           'code', 'data', 'search', 'query', 'index', 'rank']
        for pattern in math_cs_patterns:
            if pattern in name_lower:
                score += 40  # Higher boost for math/CS in science theme
        
        # Lower boost for general science patterns
        science_patterns = ['quantum', 'experiment', 'lab']
        for pattern in science_patterns:
            if pattern in name_lower:
                score += 20  # Lower boost
    
    elif theme_lower == 'scale':
        # Scale theme patterns (big, large, deep, vast, magnitude)
        scale_patterns = ['big', 'large', 'vast', 'huge', 'massive', 'deep', 'wide', 'broad',
                         'high', 'tall', 'peak', 'summit', 'apex', 'zenith', 'core', 'base',
                         'infinite', 'endless', 'boundless', 'limitless', 'scale', 'magnitude',
                         'scope', 'range', 'span', 'extent', 'volume', 'capacity', 'mega', 'macro']
        for pattern in scale_patterns:
            if pattern in name_lower:
                score += 30
    
    return max(0, score)  # Don't return negative scores

def create_word_variation(word: str) -> str:
    """Create natural variations of an English word."""
    if len(word) >= 4:
        # Try multiple variation strategies
        strategy = random.choice(['substitute', 'insert', 'delete', 'swap'])
        
        if strategy == 'substitute':
            pos = random.randint(0, len(word) - 1)
            if word[pos] in CONSONANTS:
                similar = [c for c in 'bcdfghjklmnpqrstvwxyz' if c != word[pos]]
                new_char = random.choice(similar)
                variant = word[:pos] + new_char + word[pos+1:]
                return variant
            elif word[pos] in VOWELS:
                other_vowels = [v for v in VOWELS if v != word[pos]]
                if other_vowels:
                    variant = word[:pos] + random.choice(other_vowels) + word[pos+1:]
                    return variant
        elif strategy == 'insert' and len(word) < 7:
            pos = random.randint(0, len(word))
            char = random.choice(CONSONANTS + VOWELS)
            variant = word[:pos] + char + word[pos:]
            return variant
        elif strategy == 'delete' and len(word) > 4:
            pos = random.randint(0, len(word) - 1)
            variant = word[:pos] + word[pos+1:]
            return variant
        elif strategy == 'swap' and len(word) >= 2:
            pos = random.randint(0, len(word) - 2)
            chars = list(word)
            chars[pos], chars[pos+1] = chars[pos+1], chars[pos]
            variant = ''.join(chars)
            return variant
    return word

def get_timestamp_filename(prefix: str, directory: str = '.') -> str:
    """
    Generate a timestamped filename.
    Format: YYYYMMDD_HHMMSS_{prefix}.txt
    Example: 20241231_143022_generated_domains.txt
    
    Args:
        prefix: The prefix for the filename (e.g., 'generated_domains', 'available_domains')
        directory: Directory where the file will be saved
    
    Returns:
        Full path to the timestamped file
    """
    from datetime import datetime
    
    # Get project root (parent of src directory)
    if directory == '.':
        # If relative path, resolve to project root
        src_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(src_dir)
        directory = os.path.join(project_root, directory) if directory != '.' else project_root
    elif not os.path.isabs(directory):
        # If relative path, make it relative to project root
        src_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(src_dir)
        directory = os.path.join(project_root, directory)
    
    # Generate timestamp in format YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{timestamp}_{prefix}.txt'
    return os.path.join(directory, filename)

def generate_themed_names(count: int = 500, theme: str = 'information_retrieval', min_length: int = 4, max_length: int = 8) -> list:
    """Generate names prioritizing words relevant to the selected theme."""
    names = set()
    
    print(f"Generating {count} names with theme: {theme}...")
    
    # Get theme-specific words
    theme_words = get_theme_words(theme)
    print(f"  - Using {len(theme_words)} theme-relevant words")
    
    # Method 1: Use actual theme words directly
    print("  - Using actual theme words...")
    for word in theme_words:
        if min_length <= len(word) <= max_length:
            names.add(word.lower())
    
    # Method 1b: Extract prefixes/truncations from longer words
    print("  - Extracting prefixes from longer words...")
    for word in theme_words:
        if len(word) > max_length:
            # Extract prefixes of different lengths
            for prefix_len in range(min_length, min(max_length + 1, len(word))):
                prefix = word[:prefix_len].lower()
                if min_length <= len(prefix) <= max_length and not has_awkward_vowel_ending(prefix):
                    names.add(prefix)
    
    # Method 2: Create variations of theme words
    print("  - Creating variations of theme words...")
    for word in theme_words:
        if len(word) <= max_length - 1:
            for _ in range(random.randint(2, 3)):
                variant = create_word_variation(word)
                if min_length <= len(variant) <= max_length and variant != word:
                    names.add(variant.lower())
    
    # Method 3: Combine short theme words (including 2-3 char words for more combinations)
    print("  - Combining theme words...")
    # Include 2-3 char words for more combinations (especially useful for 4-6 char limits)
    # Exclude single-letter words to avoid "queryq", "xfind" etc.
    short_theme_words = [w for w in theme_words if 2 <= len(w) <= min(5, max_length - 2)]
    # Scale iterations based on count - more iterations for higher counts
    iterations = max(count // 4, len(short_theme_words) * 10) if count > 1000 else count // 4
    for _ in range(iterations):
        if len(short_theme_words) >= 2:
            word1 = random.choice(short_theme_words)
            word2 = random.choice(short_theme_words)
            combined = word1 + word2
            if (min_length <= len(combined) <= max_length and 
                not has_awkward_vowel_ending(combined) and 
                not has_single_letter_affix(combined)):
                names.add(combined.lower())
    
    # Method 4: Add common English suffixes to theme words
    print("  - Adding suffixes to theme words...")
    suffixes = ['ly', 'er', 'ed', 'ing', 'ive', 'al', 'ic', 'est', 'ify', 'ize', 'tion', 'sion', 'ment', 'ness', 'ity', 'able', 'ible', 'fy', 'io']
    # Also include tech-style suffixes
    tech_suffixes = ['tech', 'ai', 'ml', 'io', 'ly', 'fy']
    all_suffixes = list(set(suffixes + tech_suffixes))
    base_theme_words = [w for w in theme_words if 2 <= len(w) <= max_length - 2]
    for word in base_theme_words:
        for suffix in all_suffixes:
            if len(word) + len(suffix) <= max_length:
                suffixed = word + suffix
                if min_length <= len(suffixed) <= max_length and not has_awkward_vowel_ending(suffixed):
                    names.add(suffixed.lower())
    
    # Method 5: Generate random combinations with theme word patterns (for high counts)
    if count > 10000 and len(names) < count:
        print("  - Generating random variations...")
        # Use theme words as inspiration for random generation
        for _ in range(min(count, count - len(names))):
            if short_theme_words:
                # Pick random characters inspired by theme words
                base_word = random.choice(short_theme_words)
                # Create more variations
                for attempt in range(5):
                    variant = create_word_variation(base_word)
                    if min_length <= len(variant) <= max_length and variant not in names:
                        names.add(variant.lower())
                        break
    
    # Convert to list and limit
    name_list = list(names)
    return name_list[:count]

def generate_cross_theme_names(count: int, themes: list, min_length: int = 4, max_length: int = 8) -> list:
    """Generate names by combining words from multiple themes."""
    names = set()
    
    # Get words from all themes
    all_theme_words = {}
    for theme in themes:
        theme_words = get_theme_words(theme)
        all_theme_words[theme] = [w for w in theme_words if min_length <= len(w) <= max_length]
    
    # Method 1: Combine short words from different themes
    print("  - Combining words from different themes...")
    short_words_by_theme = {}
    for theme in themes:
        # Adjust word length based on max_length constraint
        # For max_length=6, we can combine: 2+4, 3+3, 2+3, 3+2, 4+2
        max_word_len = min(4, max_length - 2)  # Leave room for second word
        min_word_len = 2
        short_words_by_theme[theme] = [w for w in all_theme_words[theme] if min_word_len <= len(w) <= max_word_len]
    
    # Scale iterations based on count
    iterations = max(count // 2, 1000) if count > 1000 else count // 2
    for _ in range(iterations):
        # Pick words from 2 different themes
        if len(themes) >= 2:
            theme1 = random.choice(themes)
            theme2 = random.choice([t for t in themes if t != theme1])
            
            if short_words_by_theme[theme1] and short_words_by_theme[theme2]:
                word1 = random.choice(short_words_by_theme[theme1])
                word2 = random.choice(short_words_by_theme[theme2])
                
                # Try both orders
                combined1 = word1 + word2
                combined2 = word2 + word1
                
                if (min_length <= len(combined1) <= max_length and 
                    not has_awkward_vowel_ending(combined1) and 
                    not has_single_letter_affix(combined1)):
                    names.add(combined1.lower())
                if (min_length <= len(combined2) <= max_length and 
                    not has_awkward_vowel_ending(combined2) and 
                    not has_single_letter_affix(combined2)):
                    names.add(combined2.lower())
    
    # Method 2: Combine theme word + suffix from another theme
    print("  - Combining theme words with suffixes from other themes...")
    for theme in themes:
        other_themes = [t for t in themes if t != theme]
        if not other_themes:
            continue
            
        # Adjust lengths based on max_length constraint
        max_base_len = max_length - 2  # Leave room for suffix
        min_base_len = 2
        base_words = [w for w in all_theme_words[theme] if min_base_len <= len(w) <= max_base_len]
        suffix_words = [w for w in all_theme_words[random.choice(other_themes)] if 2 <= len(w) <= min(3, max_length - min_base_len)]
        
        iterations = max(count // (len(themes) * 4), 200) if count > 1000 else count // (len(themes) * 4)
        for _ in range(iterations):
            if base_words and suffix_words:
                base = random.choice(base_words)
                suffix = random.choice(suffix_words)
                combined = base + suffix
                if (min_length <= len(combined) <= max_length and 
                    not has_awkward_vowel_ending(combined) and 
                    not has_single_letter_affix(combined)):
                    names.add(combined.lower())
    
    # Method 3: Three-way combinations (if 3+ themes)
    if len(themes) >= 3:
        print("  - Creating three-way theme combinations...")
        # For 3-way with max_length=6, each word should be 2 chars max
        max_word_len = max_length // 3  # Divide max_length by number of words
        iterations = max(count // 4, 500) if count > 1000 else count // 4
        for _ in range(iterations):
            selected_themes = random.sample(themes, min(3, len(themes)))
            words = []
            for theme in selected_themes:
                short_words = [w for w in all_theme_words[theme] if 2 <= len(w) <= max_word_len]
                if short_words:
                    words.append(random.choice(short_words))
            
            if len(words) >= 2:
                combined = ''.join(words)
                if (min_length <= len(combined) <= max_length and 
                    not has_awkward_vowel_ending(combined) and 
                    not has_single_letter_affix(combined)):
                    names.add(combined.lower())
    
    # Method 4: Add suffixes to cross-theme combinations
    print("  - Adding suffixes to cross-theme combinations...")
    suffixes = ['ly', 'er', 'ed', 'ing', 'ive', 'al', 'ic']
    for theme in themes:
        other_themes = [t for t in themes if t != theme]
        if not other_themes:
            continue
            
        base_words = [w for w in all_theme_words[theme] if 3 <= len(w) <= max_length - 3]
        for other_theme in other_themes:
            suffix_words = [w for w in all_theme_words[other_theme] if 2 <= len(w) <= 3]
            
            for base in base_words[:min(20, len(base_words))]:  # Limit to avoid too many combinations
                for suffix_word in suffix_words[:min(10, len(suffix_words))]:
                    combined = base + suffix_word
                    if min_length <= len(combined) <= max_length - 2:
                        for suffix in suffixes:
                            final = combined + suffix
                            if (min_length <= len(final) <= max_length and 
                                not has_awkward_vowel_ending(final) and 
                                not has_single_letter_affix(final)):
                                names.add(final.lower())
    
    # Convert to list and limit
    name_list = list(names)
    return name_list[:count]

def main():
    """Generate and score themed names."""
    print("=" * 80)
    print("THEMED DOMAIN NAME GENERATOR")
    print("=" * 80)
    
    # Create output directory if it doesn't exist (in project root, not src/)
    src_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(src_dir)
    output_dir = os.path.join(project_root, 'output')
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"📁 Created output directory: {output_dir}/")
        except Exception as e:
            print(f"  ⚠️  Could not create output directory: {e}")
            output_dir = project_root  # Fallback to project root
    
    # Get theme(s) from user
    print("\nSTEP 1: Select Theme(s)")
    print("-" * 80)
    print("Available themes:")
    print("  1. science")
    print("  2. computer_science")
    print("  3. machine_learning")
    print("  4. math")
    print("  5. information_retrieval")
    print("  6. scale (big, large, deep, vast, magnitude)")
    
    theme_choice = input("\nSelect theme(s) (1-6, comma-separated for multiple): ").strip()
    
    theme_map = {
        '1': 'science',
        '2': 'computer_science',
        '3': 'machine_learning',
        '4': 'math',
        '5': 'information_retrieval',
        '6': 'scale',
    }
    
    valid_themes = ['science', 'computer_science', 'machine_learning', 'math', 'information_retrieval', 'scale']
    
    # Parse multiple themes (only accept numbers)
    themes = []
    if ',' in theme_choice:
        # Comma-separated: "1,3,4"
        theme_choices = [t.strip() for t in theme_choice.split(',')]
        for tc in theme_choices:
            if tc in theme_map:
                themes.append(theme_map[tc])
            else:
                print(f"  ⚠️  Invalid theme number: {tc}. Skipping.")
    elif ' ' in theme_choice:
        # Space-separated numbers: "1 3 4"
        theme_choices = theme_choice.split()
        for tc in theme_choices:
            tc_clean = tc.strip()
            if tc_clean in theme_map:
                themes.append(theme_map[tc_clean])
            else:
                print(f"  ⚠️  Invalid theme number: {tc_clean}. Skipping.")
    else:
        # Single theme
        if theme_choice in theme_map:
            themes = [theme_map[theme_choice]]
        else:
            print(f"  ⚠️  Invalid theme number: {theme_choice}. Using 'information_retrieval' as default.")
            themes = ['information_retrieval']
    
    if not themes:
        print("  ⚠️  No valid themes selected. Using 'information_retrieval' as default.")
        themes = ['information_retrieval']
    
    if len(themes) == 1:
        print(f"\n✓ Selected theme: {themes[0]}")
    else:
        print(f"\n✓ Selected {len(themes)} themes: {', '.join(themes)}")
    
    # Get number of names to generate
    print("\nSTEP 2: Number of Names to Generate")
    print("-" * 80)
    print("How many names should we generate?")
    print("  (More names = more variety. Scoring and sorting are fast!)")
    print("  Recommended: 10,000-100,000 for best results")
    
    while True:
        try:
            num_names_input = input("\nEnter number of names to generate (default: 10000): ").strip()
            if not num_names_input:
                num_names = 10000
            else:
                num_names = int(num_names_input)
                if num_names < 10:
                    print("  ⚠️  Please enter at least 10 names")
                    continue
                if num_names > 500000:
                    print("  ⚠️  That's a lot! Consider a smaller number (max 500000)")
                    continue
            break
        except ValueError:
            print("  ⚠️  Please enter a valid number")
    
    print(f"\n✓ Will generate up to {num_names} names")
    print("  (Generation, scoring, and sorting are fast - this won't take long)")
    
    # Get name length constraints
    print("\nSTEP 2b: Name Length Constraints")
    print("-" * 80)
    print("What length should the names be?")
    print("  Recommended: 4-8 characters (shorter is better for domains)")
    
    while True:
        try:
            min_length_input = input("\nEnter minimum length (default: 4): ").strip()
            if not min_length_input:
                min_length = 4
            else:
                min_length = int(min_length_input)
                if min_length < 2:
                    print("  ⚠️  Minimum length must be at least 2")
                    continue
                if min_length > 15:
                    print("  ⚠️  Minimum length should be 15 or less")
                    continue
            break
        except ValueError:
            print("  ⚠️  Please enter a valid number")
    
    while True:
        try:
            max_length_input = input("Enter maximum length (default: 8): ").strip()
            if not max_length_input:
                max_length = 8
            else:
                max_length = int(max_length_input)
                if max_length < min_length:
                    print(f"  ⚠️  Maximum length must be at least {min_length}")
                    continue
                if max_length > 20:
                    print("  ⚠️  Maximum length should be 20 or less")
                    continue
            break
        except ValueError:
            print("  ⚠️  Please enter a valid number")
    
    print(f"\n✓ Name length: {min_length}-{max_length} characters")
    
    # Generate names for all selected themes
    all_names = set()
    
    if len(themes) > 1:
        # For multiple themes: generate separately AND generate cross-theme combinations
        names_per_theme = (num_names // 2) // len(themes)  # Half for individual themes
        cross_theme_count = num_names // 2  # Half for cross-theme combinations
        
        # Generate names for each theme individually
        for theme in themes:
            print(f"\nGenerating names for theme: {theme}...")
            theme_names = generate_themed_names(names_per_theme, theme, min_length, max_length)
            all_names.update(theme_names)
            print(f"  ✓ Generated {len(theme_names)} names for {theme}")
        
        # Generate cross-theme combinations (combining words from different themes)
        print(f"\nGenerating cross-theme combinations (combining words from multiple themes)...")
        cross_theme_names = generate_cross_theme_names(cross_theme_count, themes, min_length, max_length)
        all_names.update(cross_theme_names)
        print(f"  ✓ Generated {len(cross_theme_names)} cross-theme combination names")
    else:
        # Single theme: just generate normally
        names_per_theme = num_names
        print(f"\nGenerating names for theme: {themes[0]}...")
        theme_names = generate_themed_names(names_per_theme, themes[0], min_length, max_length)
        all_names.update(theme_names)
        print(f"  ✓ Generated {len(theme_names)} names for {themes[0]}")
    
    names = list(all_names)
    print(f"\n✓ Generated {len(names)} unique names total")
    
    # Score them
    print("Scoring names (theme relevance + English word score)...")
    prefs = NamePreferences()
    prefs.target_audience = 'technical'
    prefs.brand_personality = 'balanced'
    prefs.name_style = 'mixed'
    prefs.opinionated = True
    prefs.include_tech_concepts = True
    prefs.use_funded_style = True
    prefs.min_length = 4
    prefs.max_length = 8
    
    scored_names = []
    for name in names:
        # Filter out awkward vowel endings
        if has_awkward_vowel_ending(name):
            continue
        
        # Filter out bad brand patterns (suffix spam, metric salad, letter-swapped, model refs)
        if has_bad_brand_patterns(name):
            continue
        
        # Filter out single-letter affixes (queryq, findex, xfind)
        if has_single_letter_affix(name):
            continue
        
        # Filter out names ending with "ai" (redundant with .ai TLD - e.g., "searchai.ai")
        # This avoids redundant names like "linkai.ai", "searchai.ai", "rankai.ai"
        if name.lower().endswith('ai') and len(name) > 2:
            continue
        
        if is_easy_to_spell(name, prefs):
            score = score_name(name, prefs)
            english_score = score_english_word_like(name)
            primitive_score = score_primitive_verb_appeal(name)
            
            # Score against all selected themes and take the maximum
            theme_scores = [score_theme_relevance(name, theme) for theme in themes]
            theme_score = max(theme_scores)  # Use the best matching theme score
            
            # Combine scores (FIXED: reduced theme weight, prioritize primitives and English words)
            # Theme relevance reduced from 0.3 to 0.1 (was overvalued, produced too-literal names)
            # Primitives and English words get highest priority
            combined_score = score + (theme_score * 0.1) + (english_score * 0.4) + (primitive_score * 0.5)  # Theme reduced, primitives prioritized
            
            scored_names.append((name, combined_score, english_score, theme_score, primitive_score))
    
    # Sort by combined score (Primitive verbs first for domain checking priority, then English, then theme, then total)
    # Primitive verbs like "parse" should rank highest
    scored_names.sort(key=lambda x: (-x[4], -x[2], -x[3], -x[1]))  # Primitive first, then English, then theme, then total
    
    # Find max values for normalization
    max_theme = max(ts for _, _, _, ts, _ in scored_names) if scored_names else 280
    max_english = max(es for _, _, es, _, _ in scored_names) if scored_names else 175
    max_primitive = max(ps for _, _, _, _, ps in scored_names) if scored_names else 100
    max_base = max(score_name(n, prefs) for n, _, _, _, _ in scored_names) if scored_names else 200
    max_total = max(ts for _, ts, _, _, _ in scored_names) if scored_names else 250
    
    # Get max values for breakdown dimensions (calculate from actual scores)
    from generate_domain_names import (
        score_investor_appeal,
        score_engineer_appeal,
        score_executive_appeal,
        score_technical_depth,
        score_broader_appeal
    )
    
    # Calculate actual max values from the dataset (all scores are now capped at 100)
    max_investor = 100
    max_engineer = 100
    max_executive = 100
    max_technical = 100
    max_broader = 100
    
    # Save to file with normalized scores (0-100, integers)
    # Add number to prevent overwriting previous runs (1, 2, 3, etc.)
    if len(themes) == 1:
        theme_str = themes[0]
    else:
        # For multiple themes, create a combined name
        theme_str = '_'.join(themes)
    output_file = get_timestamp_filename('generated_domains', directory=output_dir)
    with open(output_file, 'w') as f:
        f.write(f"Themed Domain Name Suggestions: {theme_str}\n")
        f.write("Prioritizing theme-relevant English words\n")
        f.write("=" * 80 + "\n\n")
        f.write("SCORE DEFINITIONS:\n")
        f.write("-" * 80 + "\n")
        f.write("Theme:    How relevant the name is to the selected theme (0-100)\n")
        f.write("English:  How English-word-like the name is (100 = perfect English word)\n")
        f.write("Base:     Overall name quality score combining all dimensions (Investor + Engineer + \n")
        f.write("          Executive + Technical + Broader appeal), WITHOUT theme boost\n")
        f.write("Total:    Final ranking score = Base + (Theme * 0.3). This is what determines\n")
        f.write("          the final order (names sorted by Theme first, then Total)\n")
        f.write("\n")
        f.write("Breakdown: Individual dimension scores that make up the Base score:\n")
        f.write("  Inv:    Investor appeal (professional, credible, scalable, memorable)\n")
        f.write("  Eng:    Engineer appeal (ML/search terms, technical depth signals)\n")
        f.write("  Exec:   Executive appeal (accessible, professional, not too technical)\n")
        f.write("  Tech:   Technical depth (sophistication, algorithm relevance)\n")
        f.write("  Broad:  Broader appeal (works for both technical and non-technical audiences)\n")
        f.write("\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total names: {len(scored_names)}\n\n")
        f.write("Names sorted by theme relevance, then total score\n")
        f.write("Scores normalized to 0-100 (integers): Theme | English | Base | Total\n")
        f.write("Breakdown: Inv | Eng | Exec | Tech | Broad\n\n")
        
        for i, (name, total_score, english_score, theme_score, primitive_score) in enumerate(scored_names, 1):
            # Get base score (without theme boost)
            base_score = score_name(name, prefs)
            
            # Get individual dimension scores
            investor = score_investor_appeal(name)
            engineer = score_engineer_appeal(name)
            executive = score_executive_appeal(name)
            technical = score_technical_depth(name)
            broader = score_broader_appeal(name)
            
            # Normalize to 0-100 and convert to integers
            theme_norm = int((theme_score / max_theme) * 100) if max_theme > 0 else 0
            english_norm = int((english_score / max_english) * 100) if max_english > 0 else 0
            base_norm = int((base_score / max_base) * 100) if max_base > 0 else 0
            total_norm = int((total_score / max_total) * 100) if max_total > 0 else 0
            
            investor_norm = int((investor / max_investor) * 100) if max_investor > 0 else 0
            engineer_norm = int((engineer / max_engineer) * 100) if max_engineer > 0 else 0
            executive_norm = int((executive / max_executive) * 100) if max_executive > 0 else 0
            technical_norm = int((technical / max_technical) * 100) if max_technical > 0 else 0
            broader_norm = int((broader / max_broader) * 100) if max_broader > 0 else 0
            
            # Show .ai by default in the generated names file (before TLD selection)
            f.write(f"{i:3d}. {name}.ai\n")
            f.write(f"     Scores: Theme:{theme_norm:3d} | English:{english_norm:3d} | ")
            f.write(f"Base:{base_norm:3d} | Total:{total_norm:3d}\n")
            f.write(f"     Breakdown: Inv:{investor_norm:3d} Eng:{engineer_norm:3d} Exec:{executive_norm:3d} ")
            f.write(f"Tech:{technical_norm:3d} Broad:{broader_norm:3d}\n\n")
    
    print(f"\n✓ Saved {len(scored_names)} names to {output_file}")
    print(f"  📄 Output file: {output_file}")
    print("\nTop 30 names (prioritizing theme relevance):")
    for i, (name, total_score, english_score, theme_score, primitive_score) in enumerate(scored_names[:30], 1):
        # Show .ai by default in preview (before TLD selection)
        print(f"  {i:2d}. {name}.ai (Total: {total_score:.1f}, Theme: {theme_score:.1f})")
    
    # Optional: Check domain availability
    print("\n" + "=" * 80)
    print("STEP 3: Domain Availability Check (Optional)")
    print("-" * 80)
    print("Would you like to check domain availability using whois?")
    print("  Note: This can take a while (~1 second per domain)")
    print("  Example: Checking 100 domains takes ~2 minutes")
    
    check_availability = input("\nCheck domain availability? (yes/no, default: yes): ").strip().lower() or "yes"
    
    # Initialize variables that might be used later
    available_file = None
    available_domains = []
    
    if check_availability in ['yes', 'y']:
        # Get TLD selection
        print("\nWhich TLD(s) would you like to check?")
        print("  [1] .ai only")
        print("  [2] .com only")
        print("  [3] Both .ai and .com")
        
        tld_choice = input("\nSelect TLD(s) (1-3, default: 1): ").strip() or "1"
        
        if tld_choice == "2":
            tlds = ['.com']
        elif tld_choice == "3":
            tlds = ['.ai', '.com']
        else:
            tlds = ['.ai']
        
        print(f"\n✓ Will check domains for: {', '.join(tlds)}")
        
        # Filter out names ending with "ai" if .ai TLD is selected (avoids "searchai.ai")
        if '.ai' in tlds:
            original_count = len(scored_names)
            scored_names = [(name, score, eng, theme, prim) for name, score, eng, theme, prim in scored_names
                          if not name.lower().endswith('ai')]
            filtered_count = original_count - len(scored_names)
            if filtered_count > 0:
                print(f"  ℹ️  Filtered out {filtered_count} names ending with 'ai' (to avoid redundant .ai domains)")
        
        print("\nHow many available domains should we find before stopping?")
        print("  (We'll check names in priority order until we find this many)")
        print("  (Domain checking is slow: ~1 second per domain)")
        print("  Recommended: 50-150")
        
        while True:
            try:
                num_available_input = input("\nEnter number of available domains to find (default: 100): ").strip()
                if not num_available_input:
                    num_available = 100
                else:
                    num_available = int(num_available_input)
                    if num_available < 1:
                        print("  ⚠️  Please enter at least 1")
                        continue
                    if num_available > 500:
                        print("  ⚠️  That's a lot! Consider a smaller number (max 500)")
                        print("  (Each domain check takes ~1 second)")
                        continue
                break
            except ValueError:
                print("  ⚠️  Please enter a valid number")
        
        print(f"\n✓ Will check domains until we find {num_available} available ones")
        estimated_time = num_available * 10  # Rough estimate: check ~10x to find available ones
        print(f"  (This may check up to {min(len(scored_names), num_available * 10)} domains)")
        print(f"  (Estimated time: ~{estimated_time // 60} minutes)")
        print("\nStarting domain availability check...")
        print("  (This may take a while - checking ~1 domain per second)")
        
        # Import whois function
        from generate_domain_names import run_whois
        import time
        
        # Create cache directory if it doesn't exist (in project root, not src/)
        src_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(src_dir)
        cache_dir = os.path.join(project_root, 'cache')
        if not os.path.exists(cache_dir):
            try:
                os.makedirs(cache_dir)
                print(f"  📁 Created cache directory: {cache_dir}/")
            except Exception as e:
                print(f"  ⚠️  Could not create cache directory: {e}")
                cache_dir = project_root  # Fallback to project root
        
        # Load cache of taken domains
        cache_file = os.path.join(cache_dir, 'taken_domains_cache.txt')
        taken_domains_cache = set()
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    taken_domains_cache = {line.strip().lower() for line in f if line.strip()}
                print(f"  📋 Loaded {len(taken_domains_cache)} taken domains from cache")
            except Exception as e:
                print(f"  ⚠️  Could not load cache: {e}")
        
        # Load cache of available domains (to skip re-checking)
        available_cache_file = os.path.join(cache_dir, 'available_domains_cache.txt')
        available_domains_cache = set()
        
        if os.path.exists(available_cache_file):
            try:
                with open(available_cache_file, 'r') as f:
                    available_domains_cache = {line.strip().lower() for line in f if line.strip()}
                print(f"  📋 Loaded {len(available_domains_cache)} available domains from cache")
            except Exception as e:
                print(f"  ⚠️  Could not load available domains cache: {e}")
        
        available_domains = []
        checked = 0
        skipped = 0
        skipped_available = 0
        newly_taken = []
        newly_available = []
        max_to_check = min(len(scored_names), num_available * 10)  # Check up to 10x the target
        
        # Open cache files for incremental writing (so progress is saved if script is interrupted)
        cache_file_handle = None
        try:
            cache_file_handle = open(cache_file, 'a')
        except Exception as e:
            print(f"  ⚠️  Could not open cache file for writing: {e}")
        
        available_cache_file_handle = None
        try:
            available_cache_file_handle = open(available_cache_file, 'a')
        except Exception as e:
            print(f"  ⚠️  Could not open available domains cache file for writing: {e}")
        
        # Create a lookup for scores by name
        name_to_scores = {}
        for name, total_score, english_score, theme_score, primitive_score in scored_names:
            base_score = score_name(name, prefs)
            name_to_scores[name] = {
                'total': total_score,
                'english': english_score,
                'theme': theme_score,
                'base': base_score
            }
        
        for name, total_score, english_score, theme_score, primitive_score in scored_names:
            if len(available_domains) >= num_available:
                break
            if checked >= max_to_check:
                print(f"\n  ⚠️  Reached maximum check limit ({max_to_check}). Found {len(available_domains)} available domains.")
                break
            
            # Check each TLD for this name
            for tld in tlds:
                if len(available_domains) >= num_available:
                    break
                if checked >= max_to_check:
                    break
                
                # Skip names ending with "ai" when checking .ai domains (avoids "searchai.ai")
                if tld == '.ai' and name.lower().endswith('ai'):
                    continue
                
                domain = f"{name}{tld}"
                domain_lower = domain.lower()
                
                # Check cache first (taken domains)
                if domain_lower in taken_domains_cache:
                    skipped += 1
                    print(f"  [{checked + skipped}/{max_to_check}] {domain}... (cached - taken)")
                    continue
                
                # Check cache for available domains
                if domain_lower in available_domains_cache:
                    skipped_available += 1
                    # Get scores for this name
                    scores = name_to_scores.get(name, {})
                    available_domains.append((name, domain, "Available (from cache)", scores))
                    print(f"  [{checked + skipped + skipped_available}/{max_to_check}] {domain}... (cached - available)")
                    if len(available_domains) >= num_available:
                        break
                    continue
                
                checked += 1
                print(f"  [{checked}/{max_to_check}] Checking {domain}...", end=' ', flush=True)
                
                # Run whois with timeout handling
                is_available, status = run_whois(domain, timeout=7, retries=1)
                
                # Handle timeout/errors gracefully
                if is_available is None:
                    # Timeout or error - mark as taken to avoid re-checking immediately
                    # (but don't cache it permanently, might be temporary network issue)
                    print(f"⚠️  {status}")
                    # Continue to next domain instead of breaking
                    continue
                
                if is_available:
                    # Get scores for this name
                    scores = name_to_scores.get(name, {})
                    available_domains.append((name, domain, status, scores))
                    # Add to available cache (in-memory and file)
                    available_domains_cache.add(domain_lower)
                    newly_available.append(domain_lower)
                    # Write to cache file immediately so progress is saved if script is interrupted
                    if available_cache_file_handle:
                        try:
                            available_cache_file_handle.write(f"{domain_lower}\n")
                            available_cache_file_handle.flush()  # Ensure it's written to disk
                        except Exception as e:
                            print(f"\n  ⚠️  Could not write to available cache: {e}")
                    print(f"✓ AVAILABLE ({len(available_domains)}/{num_available})")
                elif is_available is False:
                    # Add to cache (in-memory and file)
                    taken_domains_cache.add(domain_lower)
                    newly_taken.append(domain_lower)
                    # Write to cache file immediately so progress is saved if script is interrupted
                    if cache_file_handle:
                        try:
                            cache_file_handle.write(f"{domain_lower}\n")
                            cache_file_handle.flush()  # Ensure it's written to disk
                        except Exception as e:
                            print(f"\n  ⚠️  Could not write to cache: {e}")
                    print("✗ Taken")
                # Note: None case (timeout/error) is already handled above with continue
                
                # Rate limiting (1 second delay between checks)
                time.sleep(1)
        
        # Close cache file handles
        if cache_file_handle:
            try:
                cache_file_handle.close()
                if newly_taken:
                    print(f"\n  💾 Saved {len(newly_taken)} newly found taken domains to cache")
            except Exception as e:
                print(f"\n  ⚠️  Error closing cache file: {e}")
        
        if available_cache_file_handle:
            try:
                available_cache_file_handle.close()
                if newly_available:
                    print(f"  💾 Saved {len(newly_available)} newly found available domains to cache")
            except Exception as e:
                print(f"\n  ⚠️  Error closing available cache file: {e}")
        
        if skipped > 0:
            print(f"\n  ⚡ Skipped {skipped} domains (already in cache as taken)")
        if skipped_available > 0:
            print(f"  ⚡ Skipped {skipped_available} domains (already in cache as available)")
        
        # Create filename with timestamp
        available_file = get_timestamp_filename('available_domains', directory=output_dir)
        
        # Save available domains with scores and definitions
        if available_domains:
            # Import definition function
            try:
                from add_definitions import get_definition
            except ImportError:
                # Simple fallback if add_definitions.py not available
                def get_definition(name: str) -> str:
                    """Simple definition lookup."""
                    name_lower = name.lower()
                    definitions = {
                        'search': 'to look for or find information',
                        'index': 'a list or catalog for reference',
                        'query': 'a question or request for information',
                        'rank': 'to arrange in order of importance',
                        'score': 'a numerical value or rating',
                        'parse': 'to analyze and break down into parts',
                        'extract': 'to pull out or obtain',
                        'vector': 'a quantity with direction and magnitude',
                        'tensor': 'a mathematical object generalizing vectors',
                        'cache': 'a temporary storage for quick access',
                        'filter': 'to remove or separate items',
                        'match': 'to correspond or be equal',
                        'token': 'a unit or symbol',
                        'corpus': 'a collection of texts',
                        'cluster': 'a group of similar items',
                    }
                    if name_lower in definitions:
                        return definitions[name_lower]
                    return ''
            with open(available_file, 'w') as f:
                tld_display = ', '.join(tlds)
                if len(themes) == 1:
                    f.write(f"Available {themes[0]} domains ({tld_display}) - found {len(available_domains)}\n")
                else:
                    f.write(f"Available domains ({', '.join(themes)}) ({tld_display}) - found {len(available_domains)}\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Checked: {checked} domains\n")
                if skipped > 0:
                    f.write(f"Skipped (cached): {skipped} domains\n")
                f.write("\n")
                f.write("SCORE DEFINITIONS:\n")
                f.write("-" * 80 + "\n")
                f.write("Theme:    How relevant the name is to the selected theme (0-100)\n")
                f.write("English:  How English-word-like the name is (100 = perfect English word)\n")
                f.write("Base:     Overall name quality score (combines all dimensions)\n")
                f.write("Total:    Final ranking score = Base + (Theme * 0.3)\n")
                f.write("\nBreakdown: Inv | Eng | Exec | Tech | Broad\n")
                f.write("  Inv:    Investor appeal\n")
                f.write("  Eng:    Engineer appeal (ML/search terms)\n")
                f.write("  Exec:   Executive appeal (accessible, professional)\n")
                f.write("  Tech:   Technical depth (sophistication)\n")
                f.write("  Broad:  Broader appeal (universal accessibility)\n")
                f.write("\n" + "=" * 80 + "\n\n")
                
                for i, item in enumerate(available_domains, 1):
                    if len(item) == 4:
                        name, domain, status, scores = item
                    else:
                        # Backward compatibility
                        name, domain, status = item
                        scores = name_to_scores.get(name, {})
                    
                    # Get scores
                    total_score = scores.get('total', 0)
                    english_score = scores.get('english', 0)
                    theme_score = scores.get('theme', 0)
                    base_score = scores.get('base', 0)
                    
                    # Get breakdown scores
                    investor = score_investor_appeal(name)
                    engineer = score_engineer_appeal(name)
                    executive = score_executive_appeal(name)
                    technical = score_technical_depth(name)
                    broader = score_broader_appeal(name)
                    
                    # Normalize scores
                    max_theme = 280
                    max_english = 175
                    max_base = 200
                    max_total = 250
                    max_investor = 100
                    max_engineer = 100
                    max_executive = 100
                    max_technical = 100
                    max_broader = 100
                    
                    theme_norm = int((theme_score / max_theme) * 100) if max_theme > 0 else 0
                    english_norm = int((english_score / max_english) * 100) if max_english > 0 else 0
                    base_norm = int((base_score / max_base) * 100) if max_base > 0 else 0
                    total_norm = int((total_score / max_total) * 100) if max_total > 0 else 0
                    
                    investor_norm = int((investor / max_investor) * 100) if max_investor > 0 else 0
                    engineer_norm = int((engineer / max_engineer) * 100) if max_engineer > 0 else 0
                    executive_norm = int((executive / max_executive) * 100) if max_executive > 0 else 0
                    technical_norm = int((technical / max_technical) * 100) if max_technical > 0 else 0
                    broader_norm = int((broader / max_broader) * 100) if max_broader > 0 else 0
                    
                    # Get definition
                    definition = get_definition(name)
                    
                    # Write domain with scores
                    f.write(f"{i:3d}. {domain}\n")
                    if definition:
                        f.write(f"     Definition: {definition}\n")
                    f.write(f"     Scores: Theme:{theme_norm:3d} | English:{english_norm:3d} | ")
                    f.write(f"Base:{base_norm:3d} | Total:{total_norm:3d}\n")
                    f.write(f"     Breakdown: Inv:{investor_norm:3d} Eng:{engineer_norm:3d} Exec:{executive_norm:3d} ")
                    f.write(f"Tech:{technical_norm:3d} Broad:{broader_norm:3d}\n")
                    f.write(f"     Status: {status}\n\n")
            
            print(f"\n✓ Found {len(available_domains)} available domains!")
            print(f"  📄 Available domains file: {available_file}")
        else:
            print("\n⚠️  No available domains found in the checked names.")
    
    else:
        print("\n✓ Skipping domain availability check")
        print("  You can check domains manually or use a separate script later")
    
    # Final summary
    print("\n" + "=" * 80)
    print("FILES CREATED")
    print("=" * 80)
    print(f"📄 Generated names: {output_file}")
    # Check if domain checking was done and available domains were found
    if check_availability in ['yes', 'y'] and available_file and available_domains:
        print(f"📄 Available domains: {available_file}")
    print(f"\n💡 Tip: Check {output_file} for all generated names with detailed scores")

if __name__ == '__main__':
    main()
