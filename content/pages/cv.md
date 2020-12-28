Title: Curriculum Vitae.
URL:
save_as: cv.html

<p class="text-center">
Note: for a full, up to date list of my publications, please refer to
<a href="https://scholar.google.com/citations?user=pEj09c4AAAAJ">Google Scholar</a>.
</p>

<div class="container text-center">
  <a id="prev" class="btn btn-info mx-2">Previous</a>
  <a id="next" class="btn btn-info mx-2">Next</a>
  <a href="/pdf/cv.pdf" class="btn btn-info mx-2">Download</a>
  <span>Page: <span id="page_num"></span> / <span id="page_count"></span></span>
<div id="the-container">
    <canvas id="the-canvas"></canvas>
</div>
</div>

<script type="text/javascript">
  var url = '/pdf/cv.pdf';


var pdfDoc = null,
    pageNum = 1,
    pageRendering = false,
    pageNumPending = null,
    scale = 1.6,
    container = document.getElementById('the-container');
    canvas = document.getElementById('the-canvas');
    ctx = canvas.getContext('2d');

/**
 * Get page info from document, resize canvas accordingly, and render page.
 * @param num Page number.
 */
function renderPage(num) {
  pageRendering = true;
  // Using promise to fetch the page
  pdfDoc.getPage(num).then(function(page) {
    // var viewport = page.getViewport({scale: scale});

    var viewport = page.getViewport({scale: 1});
    var scale = container.clientWidth / viewport.width;
    viewport = page.getViewport({scale: scale});

    canvas.height = viewport.height;
    canvas.width = viewport.width;

    // Render PDF page into canvas context
    var renderContext = {
      canvasContext: ctx,
      viewport: viewport
    };
    var renderTask = page.render(renderContext);

    // Wait for rendering to finish
    renderTask.promise.then(function() {
      pageRendering = false;
      if (pageNumPending !== null) {
        // New page rendering is pending
        renderPage(pageNumPending);
        pageNumPending = null;
      }
    });
  });

  // Update page counters
  document.getElementById('page_num').textContent = num;
}

/**
 * If another page rendering in progress, waits until the rendering is
 * finised. Otherwise, executes rendering immediately.
 */
function queueRenderPage(num) {
  if (pageRendering) {
    pageNumPending = num;
  } else {
    renderPage(num);
  }
}

/**
 * Displays previous page.
 */
function onPrevPage() {
  if (pageNum <= 1) {
    return;
  }
  pageNum--;
  queueRenderPage(pageNum);
}
document.getElementById('prev').addEventListener('click', onPrevPage);

/**
 * Displays next page.
 */
function onNextPage() {
  if (pageNum >= pdfDoc.numPages) {
    return;
  }
  pageNum++;
  queueRenderPage(pageNum);
}
document.getElementById('next').addEventListener('click', onNextPage);

/**
 * Asynchronously downloads PDF.
 */
pdfjsLib.getDocument(url).promise.then(function(pdfDoc_) {
  pdfDoc = pdfDoc_;
  document.getElementById('page_count').textContent = pdfDoc.numPages;

  // Initial/first page rendering
  renderPage(pageNum);
});
</script>