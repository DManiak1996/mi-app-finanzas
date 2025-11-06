---
name: postgresql
description: PostgreSQL relational database from GitHub README and documentation
---

# PostgreSQL Database Management System

Advanced object-relational database management system with source code insights

## Description

This skill provides access to the official PostgreSQL source code repository. PostgreSQL is an advanced object-relational database management system that supports an extended subset of the SQL standard, including transactions, foreign keys, subqueries, triggers, user-defined types and functions.

**Repository:** [postgres/postgres](https://github.com/postgres/postgres)
**Language:** C (84.0%)
**Stars:** 18,974
**License:** Other
**Homepage:** https://www.postgresql.org/

## When to Use This Skill

Use this skill when you need to:

- **Understand PostgreSQL internals** - Learn how PostgreSQL implements specific features at the source code level
- **Contribute to PostgreSQL** - Navigate the codebase structure and understand contribution guidelines
- **Explore core database functionality** - Study implementation of transactions, storage engines, query planning, etc.
- **Debug PostgreSQL issues** - Investigate how specific features work under the hood
- **Learn database system architecture** - Understand components like backend, optimizer, executor, storage manager
- **Extend PostgreSQL** - Create custom extensions by understanding existing contrib modules
- **Port features** - Understand how PostgreSQL implements features you want to add to another database
- **Performance optimization** - Study how PostgreSQL handles indexing, caching, and query execution

## Key Concepts

### Architecture Components

**Backend (`src/backend/`)** - Core database server components:
- **Access** - Storage access methods (heap, index, table)
- **Catalog** - System catalog management
- **Commands** - SQL command implementations (ALTER, CREATE, DROP, etc.)
- **Executor** - Query execution engine
- **Optimizer** - Query planner and optimizer
- **Parser** - SQL parsing and analysis
- **Storage** - Buffer management, file access, transaction logs
- **Utils** - Utility functions, memory management, system utilities

**Frontend (`src/bin/`)** - Client programs:
- **psql** - Interactive terminal for PostgreSQL
- **pg_dump** - Database backup utility
- **pg_basebackup** - Base backup tool
- **initdb** - Database cluster initialization

**Contrib (`contrib/`)** - Extension modules:
- Optional features and tools
- Examples: pg_stat_statements, pgcrypto, hstore, btree_gist
- Good reference for creating your own extensions

**Procedural Languages (`src/pl/`)** - Embedded language support:
- **plpgsql** - PostgreSQL's native procedural language
- **plperl**, **plpython**, **pltcl** - Perl, Python, Tcl bindings

### Build Systems

PostgreSQL supports two build systems:

1. **Autoconf/Make** (Traditional)
   - Configure with `./configure`
   - Build with `make`
   - Configuration in `configure.ac`, `GNUmakefile.in`

2. **Meson** (Modern, recommended for new development)
   - Configure with `meson setup`
   - Build with `ninja`
   - Configuration in `meson.build` files

### Development Workflow

1. **Read the guides** - Check `src/backend/README`, `src/DEVELOPERS`
2. **Find the component** - Use file_structure.md to navigate
3. **Study examples** - Look at contrib/ modules for extension patterns
4. **Test your changes** - Run regression tests in `src/test/`
5. **Submit patches** - Follow guidelines at https://wiki.postgresql.org/wiki/Submitting_a_Patch

## Quick Reference

### Database Architecture Example

Understanding how a query flows through PostgreSQL:

```c
// Query processing flow (conceptual)
// 1. Parser (src/backend/parser/) - SQL → Parse Tree
// 2. Analyzer (src/backend/parser/analyze.c) - Parse Tree → Query Tree
// 3. Rewriter (src/backend/rewrite/) - Query Tree → Rewritten Query Tree
// 4. Planner (src/backend/optimizer/) - Query Tree → Plan Tree
// 5. Executor (src/backend/executor/) - Plan Tree → Results

// Key entry point in backend/tcop/postgres.c
void exec_simple_query(const char *query_string)
{
    // Parse SQL into parse tree
    List *parsetree_list = pg_parse_query(query_string);

    // For each statement
    foreach(parsetree_item, parsetree_list)
    {
        // Analyze and rewrite
        Query *query = parse_analyze(parsetree);
        List *querytree_list = pg_rewrite_query(query);

        // Plan and execute
        PlannedStmt *plan = pg_plan_query(query);
        portal = CreatePortal(plan);
        PortalRun(portal);
    }
}
```

### Storage System Organization

```c
// Buffer management (src/backend/storage/buffer/)
// PostgreSQL uses shared buffers for caching pages

// Reading a page from disk or buffer cache
Buffer ReadBuffer(Relation relation, BlockNumber blockNum)
{
    // 1. Check if page is in shared buffers
    // 2. If not, read from disk
    // 3. Pin the buffer to prevent eviction
    // 4. Return buffer ID
}

// Writing changes to disk
void MarkBufferDirty(Buffer buffer)
{
    // Mark buffer as modified
    // Will be written by background writer or checkpointer
}
```

### Extension Module Pattern

```c
// Example from contrib/pg_stat_statements/pg_stat_statements.c
// Pattern for creating PostgreSQL extensions

#include "postgres.h"
#include "fmgr.h"

PG_MODULE_MAGIC;  // Required for all modules

// Define functions
PG_FUNCTION_INFO_V1(pg_stat_statements_reset);

Datum
pg_stat_statements_reset(PG_FUNCTION_ARGS)
{
    // Function implementation
    // Access args with PG_GETARG_xxx(0), PG_GETARG_xxx(1), etc.

    PG_RETURN_VOID();  // or PG_RETURN_xxx(value)
}

// Initialization hook
void _PG_init(void)
{
    // Called when module is loaded
    // Register hooks, allocate shared memory, etc.
}
```

### Custom Data Type Example

```c
// Pattern for creating custom data types (from contrib/citext/)

// Input function (text → internal)
PG_FUNCTION_INFO_V1(citext_in);
Datum
citext_in(PG_FUNCTION_ARGS)
{
    char *str = PG_GETARG_CSTRING(0);
    // Convert string to internal format
    // Return internal representation
}

// Output function (internal → text)
PG_FUNCTION_INFO_V1(citext_out);
Datum
citext_out(PG_FUNCTION_ARGS)
{
    // Convert internal format to string
    PG_RETURN_CSTRING(result);
}

// Define in .sql file:
// CREATE TYPE citext;
// CREATE FUNCTION citext_in(cstring) RETURNS citext ...
// CREATE FUNCTION citext_out(citext) RETURNS cstring ...
```

### B-tree Index Operation

```c
// Index operations (src/backend/access/nbtree/)
// PostgreSQL's default index type

// Insert into B-tree index
bool _bt_doinsert(Relation rel, IndexTuple itup)
{
    // 1. Find correct leaf page using binary search
    // 2. If page has space, insert tuple
    // 3. If page full, split page
    // 4. Update parent pages recursively
}

// Search B-tree index
bool _bt_search(Relation rel, ScanKey key, Buffer *bufP)
{
    // 1. Start from root page
    // 2. Binary search to find child page
    // 3. Descend tree until leaf page found
    // 4. Return buffer containing matching keys
}
```

### Transaction Management

```c
// Transaction system (src/backend/access/transam/)

// Start transaction
void StartTransactionCommand(void)
{
    // Allocate transaction ID
    // Set transaction state to IN_PROGRESS
}

// Commit transaction
void CommitTransactionCommand(void)
{
    // Write commit record to WAL
    // Flush changes to disk
    // Release locks
    // Update transaction status
}

// Rollback transaction
void AbortTransactionCommand(void)
{
    // Undo changes using MVCC
    // Release locks
    // Clean up resources
}
```

### Memory Context Pattern

```c
// PostgreSQL's memory management (src/backend/utils/mmgr/)
// Uses memory contexts to organize allocations

// Create memory context
MemoryContext ctx = AllocSetContextCreate(
    CurrentMemoryContext,
    "MyContext",
    ALLOCSET_DEFAULT_SIZES
);

// Allocate in context
MemoryContext oldcontext = MemoryContextSwitchTo(ctx);
void *ptr = palloc(size);  // Allocated in ctx
MemoryContextSwitchTo(oldcontext);

// Free entire context at once
MemoryContextDelete(ctx);  // Frees all allocations
```

### System Catalog Access

```c
// Working with system catalogs (pg_class, pg_attribute, etc.)
// From src/backend/catalog/

// Open a system catalog
Relation rel = table_open(RelationRelationId, AccessShareLock);

// Scan catalog
SysScanDesc scan = systable_beginscan(rel, indexId, true, NULL, 0, NULL);

HeapTuple tuple;
while (HeapTupleIsValid(tuple = systable_getnext(scan)))
{
    Form_pg_class classForm = (Form_pg_class) GETSTRUCT(tuple);
    // Access catalog data via classForm->...
}

systable_endscan(scan);
table_close(rel, AccessShareLock);
```

### Procedural Language (PL/pgSQL) Structure

```sql
-- Example PL/pgSQL function showing language structure
-- From contrib/ examples

CREATE OR REPLACE FUNCTION calculate_total(
    p_user_id INTEGER
) RETURNS NUMERIC AS $$
DECLARE
    v_total NUMERIC := 0;
    v_record RECORD;
BEGIN
    -- Query with cursor
    FOR v_record IN
        SELECT amount FROM orders WHERE user_id = p_user_id
    LOOP
        v_total := v_total + v_record.amount;
    END LOOP;

    -- Exception handling
    RETURN v_total;
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error calculating total: %', SQLERRM;
        RETURN 0;
END;
$$ LANGUAGE plpgsql;
```

## Available References

The skill provides access to comprehensive source code documentation:

### Core Documentation
- `references/README.md` - Project overview, building instructions, and general information
- `references/file_structure.md` - Complete repository structure (7,990 items) showing all source files, directories, and components

### Key Source Directories

**Backend Components** (`src/backend/`):
- Transaction processing, query execution, storage management
- Access methods (heap, index operations)
- Optimizer and planner
- Command implementations

**Frontend Tools** (`src/bin/`):
- psql, pg_dump, initdb, and other client utilities

**Extensions** (`contrib/`):
- 50+ optional extension modules
- Examples: amcheck, pg_stat_statements, pgcrypto, hstore, bloom filters, full-text search
- Great learning resource for extension development

**Procedural Languages** (`src/pl/`):
- PL/pgSQL implementation
- Python, Perl, Tcl language bindings

**Tests** (`src/test/`):
- Regression tests, isolation tests, recovery tests
- Performance benchmarks

**Documentation Source** (`doc/`):
- DocBook XML documentation source
- Build system for HTML/PDF documentation

## Working with This Skill

### For Beginners
1. **Start with README.md** - Understand the project structure and build process
2. **Review file_structure.md** - Get familiar with directory organization
3. **Study contrib/ modules** - Simpler, self-contained examples of extension development
4. **Read src/backend/README** - Understand backend architecture
5. **Browse src/tutorial/** - Educational examples (source code tutorials)

### For Intermediate Users
1. **Focus on specific subsystems** - Pick a component (e.g., optimizer, executor, storage)
2. **Trace query execution** - Follow code path from parser → planner → executor
3. **Study test cases** - Look at `src/test/regress/` for usage examples
4. **Read header files** - `.h` files contain excellent documentation comments
5. **Use git blame** - Understand why code was written that way

### For Advanced Users
1. **Profile performance** - Use tools like perf, gdb to analyze runtime behavior
2. **Modify planner** - Experiment with query optimization strategies
3. **Implement extensions** - Create custom data types, operators, index methods
4. **Contribute patches** - Follow submission guidelines and mailing list discussions
5. **Port features** - Study implementations to guide your own database projects

### Navigation Tips

**Finding Functions:**
- Use grep/ripgrep: `rg "function_name" src/`
- Check declarations: `rg "^function_name" src/ -g "*.h"`

**Understanding Data Structures:**
- Look in `src/include/nodes/` for node types
- Check `src/include/catalog/` for system catalog structures

**Tracing Code Paths:**
- Start at user-facing functions (e.g., `exec_simple_query`)
- Follow function calls downward
- Use `git log -S "function_name"` to see history

**Build Configuration:**
- Autoconf: `configure.ac` and `Makefile.in` files
- Meson: `meson.build` files throughout repository

## Common Patterns

### Error Handling
```c
// PostgreSQL uses ereport() for error reporting
ereport(ERROR,
    (errcode(ERRCODE_INVALID_PARAMETER_VALUE),
     errmsg("invalid input value"),
     errdetail("Value must be positive"),
     errhint("Try using a value greater than zero")));
```

### Memory Allocation
```c
// Use palloc() instead of malloc()
// Automatically freed on transaction abort
void *ptr = palloc(size);
void *ptr_zero = palloc0(size);  // Zero-initialized
pfree(ptr);  // Explicit free (optional)
```

### Concurrency Control
```c
// Use LWLocks for short-term locks
LWLockAcquire(MyLock, LW_EXCLUSIVE);
// Critical section
LWLockRelease(MyLock);

// Use heavyweight locks for longer operations
LockRelation(rel, AccessExclusiveLock);
// Long operation
UnlockRelation(rel, AccessExclusiveLock);
```

## Building PostgreSQL

### Quick Build (Unix/Linux)
```bash
# Traditional autoconf
./configure --prefix=/usr/local/pgsql
make
make install

# Modern meson (recommended)
meson setup build --prefix=/usr/local/pgsql
cd build
ninja
ninja install
```

### Running Tests
```bash
# Regression tests
make check

# Specific test
make check TESTS="test_name"

# With meson
cd build
meson test
```

## Contributing

**Before Contributing:**
1. Read `src/CONTRIBUTING.md`
2. Check PostgreSQL wiki: https://wiki.postgresql.org/wiki/Submitting_a_Patch
3. Join pgsql-hackers mailing list
4. Review coding conventions in `src/tools/pgindent/`

**Patch Workflow:**
1. Create feature branch
2. Make changes
3. Run regression tests: `make check`
4. Format code: `pgindent`
5. Create patch: `git format-patch`
6. Submit to pgsql-hackers mailing list

**Note:** PostgreSQL does NOT accept GitHub pull requests. Use the mailing list.

---

**Generated by Skill Seeker** | GitHub Repository Scraper

For official documentation, visit: https://www.postgresql.org/docs/
For contribution guidelines: https://wiki.postgresql.org/wiki/Submitting_a_Patch
