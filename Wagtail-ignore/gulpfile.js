var gulp = require('gulp');
var gutil = require('gulp-util');

var baseSrcDir = './airconapp/frontend/src/';
var baseDestDir = './airconapp/frontend/static/';


gulp.task('default', ['watch']);
gulp.task('build', ['styles', 'scripts', 'images', 'fonts', 'misc']);


/*
 * Watch - Watch files, trigger tasks when they are modified
 */
gulp.task('watch', ['build'], function () {
	gulp.watch(baseSrcDir + 'scss/**', ['styles']);
	gulp.watch(baseSrcDir + 'images/**', ['images']);
	gulp.watch(baseSrcDir + 'javascript/**', ['scripts']);
	gulp.watch(baseSrcDir + 'fonts/**', ['fonts']);
	gulp.watch(baseSrcDir + 'misc/**', ['misc']);
});


/*
* Scripts
*/
gulp.task('scripts', ['scripts:compile', 'scripts:jshint']);


/*
* compile - Use Browserify to compile and move JavaScript
*/
var buffer = require('vinyl-buffer');
var source = require('vinyl-source-stream');
var browserify = require('browserify');
var uglify = require('gulp-uglify');

gulp.task('scripts:compile', function(){
	return browserify(baseSrcDir + 'javascript/app.js')
		.bundle()
		.pipe(source('app.js'))
		.pipe(buffer())
		.pipe(uglify())
		.pipe(gulp.dest(baseDestDir + '/js'))
		.on('error', gutil.log);
});


/*
* jshint - Ensure our JavaScript is pretty lookin
*/
var jshint = require('gulp-jshint');
var stylish = require('jshint-stylish');

gulp.task('scripts:jshint', function(){
	gulp.src(baseSrcDir + 'javascript/app.js')
		.pipe(jshint({esnext: true}))
		.pipe(jshint.reporter(stylish))
		.on('error', gutil.log);
});


/*
 * Images - Compress and move images
**/
var changed = require('gulp-changed');
var imagemin = require('gulp-imagemin');

gulp.task('images', function () {
	return gulp.src(baseSrcDir + 'images/**')
		.pipe(changed(baseSrcDir + 'images/**')) // Ignore unchanged files
		.pipe(imagemin()) // Optimize
		.pipe(gulp.dest(baseDestDir + 'images/'))
		.on('error', gutil.log);
});


/*
* Fonts - Move font files
* */
gulp.task('fonts', function () {
	return gulp.src(baseSrcDir + 'fonts/*')
		.pipe(gulp.dest(baseDestDir + 'fonts/'))
		.on('error', gutil.log);
});


/*
 * Copy misc files across
 */
gulp.task('misc', function() {
	return  gulp.src(baseSrcDir + 'misc/*')
	.pipe(gulp.dest(baseDestDir + 'misc/'))
	.on('error', gutil.log);
});


/*
 * SASS - Compile and move sass
**/
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var autoprefixer = require('gulp-autoprefixer');
var pixrem = require('gulp-pixrem');
var minifyCss = require('gulp-minify-css');

gulp.task('styles', function() {
	var scssSources = [
		baseSrcDir + 'scss/app.scss',
	];
	return gulp.src(scssSources)
		.pipe(sourcemaps.init())
		.pipe(sass({
			outputStyle: 'expanded',
			errLogToConsole: true
		}))
		.pipe(autoprefixer({
			browsers: ['last 2 versions'],
			cascade: false
		}))
		.pipe(pixrem())
		.pipe(minifyCss())
		.pipe(sourcemaps.write('./maps'))
		.pipe(gulp.dest(baseDestDir + 'css/'))
		.on('error', gutil.log);
});
