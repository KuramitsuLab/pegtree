var gulp = require('gulp');
var gutil = require('gulp-util');
var gtypescript = require('gulp-tsc');
var gjade = require('gulp-jade');

gulp.task('default', function(){
    gulp.src(['index.ts'])
        .pipe(gtypescript())
        .pipe(gulp.dest("."));
    gulp.src(['jade/index.jade'])
        .pipe(gjade())
        .pipe(gulp.dest("."));
});
