typedef struct FBProcessTimes {
	double beginUserCPUElapsedTime;
	double beginSystemCPUElapsedTime;
	double beginIdleCPUElapsedTime;
	double beginApplicationCPUElapsedTime;
} FBProcessTimes;

typedef struct os_unfair_lock_s {
	unsigned _os_unfair_lock_opaque;
} os_unfair_lock_s;
